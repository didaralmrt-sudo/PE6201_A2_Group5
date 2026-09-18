# Contributions

Group 5 — NTU PE6201 Assessment 2 (Problem A: health-insurance claims triage agent)

This document maps each team member to the modules they owned, so the commit
history can be read against the assignment's D0–D7 breakdown.

| Member | D-ranges | Responsibility | Primary files |
|--------|----------|----------------|---------------|
| M1 | D1, D2(a), D2(c) | Single-agent ReAct control loop; the 7-tool set; single-turn multi-tool parallelism and its measurement | `A2_scaffold/agent.py`, `A2_scaffold/agent_sequential.py`, `A2_scaffold/run_d2c.py`, `A2_scaffold/tools.py` (tool set), `A2_scaffold/config.py` |
| M2 | D2(b), D3(a) | Six-field descriptor rewrite (v1 → v2); guardrail code layer (turn / budget / duplicate / autonomy gate) | `A2_scaffold/tools.py` (descriptors), `A2_scaffold/prompt.py`, `A2_scaffold/guardrails.py` |
| M3 | D4, D5(a) | Evaluation-set framework; scripted, reproducible harness; vendor-neutral backend replay | `A2_scaffold/harness.py`, `A2_scaffold/run_eval.py`, `A2_scaffold/backends.py` (SCRIPTS), `A2_reference_data/check_my_data.py` |
| M4 | D3(b), D7 | Guardrail checklist (≥10 items, ≥3 hostile); two-failure reproduction (runaway loop, duplicate-action loop) | `A2_scaffold/guardrails.py` (`check_turns` / `check_duplicate`), `M4_guardrail_test.py`, `appendix/M4_D3b_guardrail_checklist.md`, `appendix/M4_D7_failures.md` |
| M5 | D0(a)(b)(c) | "Why an agent" justification; five D0(c) statements | `M5_Cases/`, `appendix/M5_*` (report §1) |
| M6 | D6, §4, §6, video | Three-layer cost model; four levers and break-even; "what we would not deploy" | `M6_Cases/`, cost notebook, `appendix/M6_*` |

All six members also authored 6–7 evaluation cases each (merged into
`A2_scaffold/backends.py` SCRIPTS, `A2_reference_data/data_A/claims.json`,
`expected_outcomes_A.json`) and ran one live model each.

## Contributor handles observed in history

`zkai023`, `didar.almrt`, `jintingli2004`, `TyyCheN`, `nofear777tx`.
The team should confirm the exact handle → person mapping; the module ownership
above is the grading-relevant part and is reflected in the commit log by area.

## Commit convention

Every change is scoped to one module and referenced by its D-number in the
commit message (e.g. "补齐 backends 中 8 个缺脚本的案例"), so a reviewer can
map each commit to a deliverable.
