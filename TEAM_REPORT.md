# PE6201 A2 — Group 5 · Team Report (Problem A)

Six sections, fixed order, ≤2000 words total. Each section is authored by the
member named in its heading; the section budgets are §1≤400 §2≤450 §3≤350
§4≤400 §5≤250 §6≤150.

---

## §1 — Why an Agent (M5, D0)

Problem A is the first-response assessment of a health-insurance claim: given a
claim record, decide approve-in-principle, request-document, or escalate, and
record the facts that justify it. The decision is never a single lookup. It is a
short chain of tool calls — read the claim, pull the member's policy, test each
line for coverage and pre-authorisation, check for a duplicate prior decision —
that ends in a branch. The branch is data-dependent: whether
`get_preauthorisation` is even called depends on a flag `check_coverage` returns.
That dependency, evaluated at machine speed against a system of record that can
contradict the model, is exactly what rules out the lower rungs.

**Where the rungs land.** A single prompt (rung 1) cannot hold the policy,
coverage and duplicate data, and cannot act on a branch it cannot compute. A
fixed workflow (rung 2) handles the happy path but shatters when a document is
missing or a policy has lapsed — the cases that dominate the costly tail.
Read-only retrieval (rung 3) can answer "what does the policy say" but cannot
produce a decision record or route a duplicate. The ReAct agent with tools and
guardrails (rung 4) is the first rung that does the whole job: it calls the
tools, reads their answers, then commits. Rungs 5–6 (a critic agent, or
human-in-the-loop) add a verification pass at the cost of a second loop per
claim; the failures we see are wording issues, so the rung is not yet warranted
(Section 6).

**The two tests.** First, is there a system of record that can contradict the
model at machine speed? Yes — policy, coverage, pre-authorisation and
prior-decision data, all read by tools, not memorised. Second, the autonomy
equation *s = P^(1/T)*: the probability a single step is safe, raised to the
number of steps. Our agent keeps *T* small by parallelising independent calls in
one turn (Section 2), so *s* stays high without handing the model an
irreversible action.

**What good looks like.** The scripted harness reproduces 100% pass on an
isolated, outcome-graded, multi-trial set; the negative cases — lapsed policy,
out-of-window, over-limit, duplicate, prompt injection — are caught rather than
waved through; and the one irreversible step sits behind a gate that logs its
evidence trail.

---

## §2 — The Tool Layer (M1 + M2, D2(a)/D2(b)/D2(c)/D3(a))

**§2.1 Tool set & parallelism (M1, D2(a)/D2(c)).** Tools are our only path to
ground truth — each answers a question the model cannot answer from memory. The
assignment lists six minimum tools for Problem A; the scaffold ships seven: the
six required (`get_claim`, `lookup_policy`, `check_coverage`,
`get_preauthorisation`, `lookup_hospital`, `issue_decision_letter`) plus
`check_duplicate_claim`, which the duplicate family makes mandatory.

Before keeping a tool we tried the cheaper moves the brief prescribes.
`check_coverage` returns `requires_preauth` and `excluded` in one call, so no
separate exclusion tool is needed. We tested deleting `lookup_hospital` and
kept it because the record must state panel status. That negative result —
nothing removable without breaking a required outcome — is the evidence the
brief asks for. `get_preauthorisation` is the cost we scrutinised hardest
(called on ~1/3 of claims); we keep it because removing it fails every pre-auth
case.

Parallelism comes from the data, not the code: two calls share a turn only if
neither needs the other's output. In Problem A the policy and hospital lookups,
every coverage check, and the duplicate check need only `get_claim`'s fields, so
they run in one turn; only `get_preauthorisation` waits on the coverage answers.
Measured on the 7-case D2(c) set, parallel uses **22 turns against 43
sequential — 49% fewer** — pass rate unchanged (7/7 both). On the shipped
60k-token budget the sequential multi-line cases trip the budget-cap guardrail,
so parallel calling keeps long claims inside the safety ceiling.

**§2.2 Descriptors & the guardrail code layer (M2, D2(b)/D3(a)).** Every tool
carries a **six-field descriptor** (does/reads/returns; what "returns None" means
in business terms; the mistake it prevents; its signature). That last field is
the poka-yoke: `check_coverage` demands a `policy_id`; `get_preauthorisation` is
"call ONLY when `requires_preauth` is true," because the model's classic error
is calling it on every line. The descriptors feed `prompt.build_system_prompt()`
and are resent every turn, so length must earn its keep.

That makes the rewrite **measurable**. We wrote a worse v1 (verbose, no
poka-yoke) and a v2 (tight, with the "returns None means request the reference,
not refuse" rule and the call-only-when-flagged guard). `python run_eval.py
--prompt` prints the exact prompt and size, so the v1→v2 diff is what we measured:
v2 is shorter and, on guardrail cases, passes where v1 let the model call
`get_preauthorisation` indiscriminately. **[pending: M2 to run v1 and v2 on the
same model and record the trials / passed / pass-rate here — see
appendix/M2_v1_v2.md; the live v1/v2 run on M3's Llama is still to be done.]**

The guardrails live in **code** (`guardrails.py`): `check_turns`, `check_budget`,
`check_duplicate` and `gate` each raise `GuardrailStop` on violation; the agent
records `stopped_by` and escalates. The D3(b) checklist (12 cases, ≥3 hostile)
and `M4_guardrail_test.py` (7/7) exercise this layer.

---

## §3 — What the Evidence Showed (M3, D4 + D5(a))

Our evaluation set is **isolated, outcome-graded and multi-trial** — the
properties the brief requires. It totals **40 cases**: 7 provided by the
assignment and 33 authored by the team (7 each from M1–M4, 6 each from M5–M6),
spread across the problem's families — single- and multi-line runs,
pre-authorisation present/absent/expired, exclusions, policy lapsed / out-of-window
/ over-limit, duplicate-of-decided, required-document-absent, and overt plus
imitating-tool-output prompt injection. Each case asserts both the decision and,
where relevant, the trigger label and the must-record fields, so a pass means
the right outcome for the right reason, not a lucky default.

On the **scripted backend** the marker command `python run_eval.py` reproduces
the set at **100% pass (88/88 trials** — the 40 cases run with 3 trials on the
negative families). This is the number a clean clone must reproduce, and it is
stable because the scripted backend replays fixed answers and costs nothing. The
negative cases are where the set earns its keep: the escalate and refuse families
(lapsed, out-of-window, over-limit, duplicate, missing-document) are caught and
recorded with their triggers; the prompt-injection families are escalated rather
than obeyed.

The **live battery** is where the models diverge, and it is the honest part of
the evidence. Each member runs the same v2 set through their own OpenRouter model
(six models across at least two price tiers, no two from the same family). The
measured live pass rates are now in `SELF_ASSESSMENT.md`: **claude-haiku-4.5
91.7%** (M6), **deepseek-chat 78.7%** (M5), **qwen-2.5-7b 40.7%** (M4),
**gpt-4o-mini 24.2%** (M1, 33 trials), **llama-3.1-8b 4.6%** (M3). The failures
cluster in **trigger-label wording** — the model reports `lapsed` where the key
expects `policy_lapsed`, or `date_of_service` for `outside_policy_dates`. The
decision is usually correct; only the label differs. That is a prompt-engineering
target, not broken logic, and it is exactly the divergence the battery is designed
to surface.

---

## §4 — What It Costs (M6, D6)

The cost model has four levers the brief names; we state which dominated.
**Problem A runs at 8,000 claims per month** (assignment volume), with a default
failure cost of a claims assessor at US$38/hour for 12 minutes ≈ **US$7.60 per
claim that the agent misroutes to a human**.

- **Lever 1 — input price.** Cheap tier ≈ US$0.10 / M tokens. A single run is
  ~12 turns ≈ 43,200 input tokens, so input alone is ~US$0.0043/run.
- **Lever 2 — output price.** Cheap tier ≈ US$0.40 / M tokens; output is the
  expensive side — 4× input on the cheap tier. Output price scales cost fastest
  as we move up tiers.
- **Lever 3 — caching.** The prompt (system + seven descriptors) is resent every
  turn, so input compounds with turns. We do **not** yet cache the static system
  prompt; adding prompt caching would cut input on the long multi-line cases.
- **Lever 4 — reasoning model.** We use none; the cheap tier handles the chain.
  A reasoning model would add reasoning tokens and break the budget.

**Dominant lever: output price × turns**, amplified by the per-turn prompt
resend (so descriptor length compounds on input). At the cheap tier a run costs
≈ US$0.005; across 8,000 claims that is ≈ **US$40/month variable**, plus the
fixed layer (storage, infra, eval runs, monitoring). On the mid tier (≈
US$0.049/run) it is ≈ **US$392/month** — a 10× swing driven entirely by lever 2.

**Sensitivity & break-even.** Volume ±50% moves the monthly by the same factor;
the price tier (cheap↔mid) moves it 10×. Break-even against the human fallback
is trivial: even at the mid tier, US$0.049/run is ~150× cheaper than the US$7.60
a misrouted claim costs a human. The real saving depends on the live pass rate
(Section 3), not the price tier. **[Measured live-battery totals are in
SELF_ASSESSMENT.md — per-run cost ranged from US$0.015 (llama) to US$1.63
(haiku), driven by output tokens and tier.]**

---

## §5 — The Two Failures (M4, D7)

Both failures were found by **instrumentation, not assumption**: turns and cost
are logged per run, so a runaway loop shows as a turn count that never closes.

**Failure 1 — runaway loop.** Without a step cap the agent calls tools forever
and never closes; inside the token budget it hits the ceiling and burns money.
Root cause: no termination guardrail, or one that did not interrupt.
Reproduction: a 20-step same-call script trips `step_cap` at turn 9 (MAX_TURNS =
8). Fix: `Guardrails.check_turns` raises `GuardrailStop("step_cap")` when
`turn > max_turns`; the agent records `stopped_by` and escalates. Before/after:
an unbounded loop becomes a loud, logged stop with a decision on the record.

**Failure 2 — duplicate-action loop.** The agent repeats the same call with the
same arguments and makes no progress — eight turns, no conclusion, ~1.6× cost.
Root cause: no de-duplication. Reproduction: `M4_guardrail_test.py` case 6 —
`get_claim` called twice with identical args trips `duplicate_action`. Fix:
`Guardrails.check_duplicate` signs each call as `(tool, repr(sorted(args)))` and
raises `GuardrailStop` on a hit; the agent escalates.

Both live in **code, not the prompt** — the loop failure in the agent-control
layer, the duplicate in the guardrail layer — so they are reproducible and fixed
by a raised exception, not a wording change. The D3(b) checklist (12 cases, ≥3
hostile) and `M4_guardrail_test.py` (7/7) keep the layer honest.

---

## §6 — What We Would Not Deploy (M6, D0 limit)

The limit we found is fragility in the live model's **labelling**, not its
reasoning: trigger words drift (`lapsed` vs `policy_lapsed`) and prompt injection
is only partly caught. The agent is sound on scripted; it is brittle on wording.

The architecture we did not build is a second **critic agent** that re-checks the
decision and its trigger label before the gate. What it would catch: the label
mismatches that cost us pass rate, likely lifting the live figure above 24.2%.
What it would cost: one extra agent pass per claim — roughly doubling turns and
tokens (≈ +US$80/month at the cheap tier) and latency. We stayed single-agent
because the failure is a wording issue, not a reasoning gap, so a
descriptor-and-prompt fix is cheaper than a second loop; if the live battery
shows the gap persisting across models, the critic is the next rung to add.
