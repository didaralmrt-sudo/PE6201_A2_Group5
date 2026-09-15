# Section 2 — The Tool Layer (M1)

We use tools as our only way to reach ground truth. The model
cannot know a member's policy or a procedure's coverage from memory, so
every tool answers one question the model cannot.

**The tool set we ship.** The assignment lists six tools as the minimum
for Problem A. The scaffold we were given already ships seven: the six
required tools (`get_claim`, `lookup_policy`, `check_coverage`,
`get_preauthorisation`, `lookup_hospital` — which the brief names
`get_hospital_status` — and `issue_decision_letter`) plus
`check_duplicate_claim`. M1 did not add tools; our task was to document
and justify the set we were given.

**Why this set, not a bigger one.** Before keeping any tool we tried the
cheaper moves the brief suggests. `check_coverage` already returns both
`requires_preauth` and `excluded` in one call, so we need no separate "is
this excluded" tool. We tested deleting `lookup_hospital`: we kept it
because the decision record must *state* the hospital's panel status, and
a run that never checked it fails the judgement check. That negative
result — we found no tool we could remove without breaking a required
outcome — is the evidence the brief asks for.

**What each tool does.** `get_claim` runs alone on turn 1; everything
else needs its output. `lookup_policy` gives the three escalate reasons
(lapsed, out-of-window, over limit). `check_coverage` runs once per line
and is the branch point: `requires_preauth` decides whether a later
lookup happens at all, and `excluded` refuses one line without escalating
the whole claim. `get_preauthorisation` returns None for two different
reasons — never granted, or expired — and None means "request the
reference", not "refuse". `check_duplicate_claim` matches on all four
facts (member, hospital, date, lines), not the claim id, because a
resubmission arrives with a new id. `issue_decision_letter` is the one
irreversible step and sits behind the autonomy gate.

**Parallelism comes from the data, not the code.** Two calls share a turn
only if neither needs the other's output. In Problem A the policy and
hospital lookups, every per-line coverage check, and the duplicate check
all need only fields from `get_claim`, so they run in one turn. The only
call that cannot join is `get_preauthorisation`, because the set of lines
needing it is decided by the coverage answers. D2(c) runs the full set
both ways: parallel uses 22 turns against 43 sequential — 49% fewer —
with token spend down 62% and pass rate unchanged. On the shipped
60k-token budget the sequential versions of the multi-line cases trip the
budget-cap guardrail and escalate, so parallelism is not merely cheaper;
it keeps long claims inside the safety ceiling.
