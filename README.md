# PE6201 A2 — Group 5 · Problem A (Health-Insurance Claims Triage Agent)

An LLM-agent system that first-responds to a health-insurance claim: it reads the
claim, pulls the member's policy, tests each line for coverage and
pre-authorisation, checks for a duplicate prior decision, then decides
**approve-in-principle / request-document / escalate** and records the facts that
justify it — behind guardrails (step cap, token budget, de-duplication, an
autonomy gate on the one irreversible action).

This repository is the full, runnable submission: code, evaluation set, the
six-member live battery, the team report and the self-assessment.

---

## 1. Prerequisites

- **Python 3.10+** (we developed on 3.13). The scaffold uses **only the Python
  standard library** — there is **nothing to `pip install`**.
- **Live mode only** (optional, costs money): an OpenRouter API key in the
  environment variable `OPENROUTER_API_KEY`. The **scripted** mode — which is the
  default and the one a clean clone must reproduce — needs **no key** and makes
  **no network call**.

```bash
# Linux / macOS
export OPENROUTER_API_KEY="sk-or-..."

# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-or-..."
```

> **A marker clones this repository and runs it scripted. That must work with zero
> setup.** If it does not, Technical Execution (D5a) is capped. Test it the way a
> marker will: clone into a fresh folder and run there.

---

## 2. Quick start — clone and run (the scripted battery)

```bash
git clone https://github.com/didaralmrt-sudo/PE6201_A2_Group5.git
cd PE6201_A2_Group5
cd A2_scaffold
python run_eval.py
```

Expected output (verified on a clean machine):

```
BACKEND=scripted  FREE, deterministic  |  PROBLEM=A  |  model=(no model)  |
 cap=8 turns  |  autonomy=confirm

  Running the 48 SCRIPTED case(s): CLM-8842, CLM-8850, ...
  ...
====================================================================
  RESULTS   108 of 108 trials passed   (100%)
====================================================================
  trials              108
  median turns        2.0
  worst case turns    5
  hit the step cap    0
  total cost          US$0.0346   (scripted backend)

  Every trial passed the code check.
  That is HALF the check. Work through the judgement queue
  before you believe this number.
```

- **48 cases, 108/108 trials pass (100%).** The scripted backend replays fixed
  answers, so this number is **deterministic and identical on any machine** — it
  does not depend on a model, a key, or the network.
- The scripted backend **never reads the prompt**, so a prompt change cannot make
  the scripted number move. (This is what makes the run reproducible for D5a.)

> **Reading the output.** The run prints two checks:
> 1. **CODE CHECK** — automated; every trial must pass. This is the `108/108`.
> 2. **JUDGEMENT CHECK** — a short queue of items a *human* reads per case (e.g.
>    "did the reason capture the missing document?"). It is printed for single-case
>    runs and is **not** a failure when you see it listed.

---

## 3. Running a single case (verbose)

```bash
python run_eval.py CLM-8842
```

This runs one case and prints every turn, the decision record, the `CODE CHECK`
result, and the `JUDGEMENT CHECK` queue for that case. Useful for grading an
individual scenario or debugging.

---

## 4. Optional — live mode (costs money)

Live mode calls a real model through OpenRouter and is billed to your key. It is
only needed for the model battery (D5b), not for the reproducible run.

1. Set the key (see §1).
2. Edit `A2_scaffold/config.py`:

```python
BACKEND = "live"                       # "scripted" | "live"
MODEL   = "openai/gpt-4o-mini"         # any OpenRouter model id
```

3. Run the same entry point:

```bash
python run_eval.py            # live over the scripted case set
python run_eval.py --all      # live over every case in the work queue
```

> **Do not commit `config.py` with `BACKEND="live"`.** The submitted default must
> stay `BACKEND="scripted"` so a clean clone runs for free. Revert it before
> committing (`git checkout -- A2_scaffold/config.py`).

For running the whole six-member battery (or letting a notebook manage the model),
use `A2_live_battery.ipynb` — its setup cell pulls the latest scaffold and runs
every case for the chosen model.

Optional: point the data directory elsewhere with `A2_DATA=/path/to/A2_reference_data`.

---

## 5. Data sanity check

Before trusting the numbers, confirm the reference data is internally consistent:

```bash
cd A2_reference_data
python check_my_data.py
```

Expected: a per-table breakdown ending in `Your data hangs together.`

---

## 6. Repository layout

```
A2_scaffold/             the agent code
    run_eval.py          ENTRY POINT — a marker runs this (scripted by default)
    agent.py             ReAct control loop (parallel & sequential runners)
    tools.py             the 7-tool contract + Problem A/B descriptors
    guardrails.py        step cap / token budget / duplicate / autonomy gate
    prompt.py            system-prompt builder + audit()
    backends.py          SCRIPTS (fixed answers) + live backend
    harness.py           case loader, runner, reporter
    config.py            the only file that knows which model (D5)
A2_reference_data/       fixtures (next to the scaffold)
    data_A/              claims.json, members.json, policies.json,
                         preauthorisations.json, procedures.json,
                         hospitals.json, required_documents.json,
                         decided_claims.json
    data_B/              referral-coordination fixtures
    expected_outcomes_A.json / expected_outcomes_B.json
    check_my_data.py     consistency check
    data_dictionary.json
M5_Cases/ M6_Cases/   per-member case + key material
                         (M1–M4 case inputs are merged into A2_reference_data)
appendix/                per-member reports & evidence (M1–M6)
results_live_*.json     each member's live-battery run (on OpenRouter)
TEAM_REPORT.md           the six-section team report (≤2000 words)
SELF_ASSESSMENT.md      per-member model, live pass rate, case count
CONTRIBUTIONS.md         member → module / commit mapping
video/                  where the demo video is submitted (see video/README.md)
```

> **Windows filename warning.** Never create result-file names containing a colon
> (`:`) — it is a reserved character and will make the repo un-cloneable for other
> Windows users. Model names in result files use a hyphen instead, e.g.
> `results_live_M4_qwen-qwen-2.5-7b-instruct.json`.

---

## 7. Key commands

| Goal | Command (from `A2_scaffold/`) |
|------|-------------------------------|
| Reproduce the scripted set (default) | `python run_eval.py` |
| Run every case in the work queue | `python run_eval.py --all` |
| Run one case, verbose | `python run_eval.py CLM-8842` |
| Print the exact prompt and stop | `python run_eval.py --prompt` |
| Check data consistency | `cd ../A2_reference_data && python check_my_data.py` |

---

## 8. Report & assessment

- **Team report** — `TEAM_REPORT.md` (§1 Why an Agent · §2 Tool Layer ·
  §3 Evidence · §4 Cost · §5 Two Failures · §6 What We Would Not Deploy).
- **Self-assessment** — `SELF_ASSESSMENT.md` (each member's model, live pass
  rate, case count).
- **Contributions** — `CONTRIBUTIONS.md` (member → module / commit mapping).

---

## 9. Note on reproducibility

The scripted backend is the contract with the marker: it replays `SCRIPTS` from
`backends.py` and compares against `expected_outcomes_A.json`. Add a case by
appending to `SCRIPTS` and to `data_A/claims.json`; the next `python run_eval.py`
will replay it. A clean clone therefore reproduces the battery exactly, which is
the whole point of D5a.

---

## 10. What Good Looks Like (D0c Criteria for Problem A)

1. **Traceable Cause:** The final decision (e.g., escalating due to exceeded annual limit) must name the real cause traceable directly to a system record, rather than a plausible story fabricated by the model.
2. **Consistent Outcome:** The approved and refused line-item totals in the decision log must be strictly consistent with the underlying coverage status and pre-authorisation validity of each `procedure_code`.
3. **Single Gated Action:** The system takes the irreversible gated action (`issue_decision_letter`) at most once, only after all facts are established, and strictly behind the `confirm` autonomy gate.
4. **Honest Escalation:** The system says "I don't know" and safely escalates rather than inventing an answer when faced with manipulative patient narratives or complex claims lacking explicit rule coverage.
5. **Cost-Effective:** The average cost per successful task, including the expected fallback cost of failure, must be strictly less than the cost of a human claims assessor doing it (US$7.60).
