# M1 · D2(a) — Three-Question Scorecard for the Problem-A Tool Set

One row per tool. The three questions are the ones the brief asks you to
answer for every tool you ship. The "never-called cost" in Q3 is the
descriptor's token size (measured from `tools.DESCRIPTORS`) **times the
number of turns it sits in the prompt**, because the prompt is re-sent
every turn. A tool that is rarely used but always present is dead weight
on every turn — that is exactly the pressure behind "the shortest
defensible tool set: four well-justified tools beat eleven."

Descriptors were measured with `len(json.dumps(d)) // 4 + 1` (≈tok/4 heuristic).

| # | Tool | Q1 — Which task FAILS if this tool is removed? | Q2 — Could the model confuse it with a neighbour? | Q3 — Cost when NEVER called (per 4-turn run) |
|---|------|-----------------------------------------------|--------------------------------------------------|----------------------------------------------|
| 1 | `get_claim` | The entire run. Everything (member, hospital, lines) derives from it. Turn 1 must run alone. | Low. Unique name, unique output shape. | ~127 tok × 4 = ~508 tok. But it is ALWAYS called, so this is a non-issue. |
| 2 | `lookup_policy` | Cannot test lapsed status, policy dates, annual-limit headroom, or exclusions. ≈ every escalate/refuse case fails. | Medium. `lookup_policy` vs `lookup_hospital` both "lookup_*" and both return dicts; kept distinct by args (`member_id` vs `hospital_id`) and by descriptor. | ~179 tok × 4 = ~716 tok. Always needed, non-issue. |
| 3 | `lookup_hospital` | No — decision is unchanged (panel status only changes what the *record says*, not the outcome). BUT the judgement check requires the panel status to be stated, so a run that never checked it fails the judgement check. | Medium. Confusable with `lookup_policy` (see above). | ~113 tok × 4 = ~452 tok. Always called, non-issue. |
| 4 | `check_coverage` | Cannot dispose any line item. Every multi-line claim fails. Called ONCE PER LINE. | **High.** Confusable with `get_preauthorisation` (both key on a procedure code). Mitigated by the descriptor: "ONLY when `check_coverage` said `requires_preauth` is true." | ~178 tok × 4 = ~712 tok. Always called per line, non-issue. |
| 5 | `get_preauthorisation` | Cannot resolve the `request_document` outcome for a line that needs pre-approval. | **High.** The model's classic error is calling it for EVERY line. The descriptor explicitly says: call ONLY when `requires_preauth` is True, else you did not read the flag. | ~202 tok × 4 = ~808 tok. **Only needed on ~1/3 of claims** (those with a `requires_preauth` line). On the other 2/3 this is pure dead weight every turn — the strongest "shortest set" candidate to watch. |
| 6 | `check_duplicate_claim` | Cannot catch a resubmission of an already-decided claim → silent wrong approve. The Appendix-A data ships 4 near-miss history rows that punish any shortcut match. | Medium. Confusable with `check_coverage` (both "check_*"). Kept distinct by args (4 facts vs code+policy). | ~166 tok × 4 = ~664 tok. Needed on every claim (duplicate check is universal), so justified. |
| 7 | `issue_decision_letter` | Cannot complete the gated irreversible step — the run never terminates with a decision. | Low. Unique name, unique role (the gated action). | ~180 tok × 4 = ~720 tok. Always the last call, non-issue. |

## "Shortest defensible set" — what we kept, what we considered cutting

- **Kept all six brief-mandated tools** (`get_claim`, `lookup_policy`,
  `check_coverage`, `get_preauthorisation`, `lookup_hospital`,
  `issue_decision_letter`) plus `check_duplicate_claim`, which the
  Appendix-A duplicate family makes mandatory.
- **Candidate for deletion we evaluated: `lookup_hospital`.**
  Observation that kept it: the routing table and the decision-record
  template require panel status to be *stated*; an agent that never
  checked it produces a record that fails the judgement check. So it
  stays. (Honest report: we tried the "four moves before adding a tool"
  discipline and found no tool we could delete without breaking a
  required outcome — that negative result is itself the evidence the
  brief asks for.)
- **`get_preauthorisation` is the one tool we scrutinised hardest** (Q3):
  it earns its ~800 tok/run only on claims whose lines `requires_preauth`.
  We keep it because removing it would make every pre-auth case fail, but
  we note it is the largest "always-in-prompt, rarely-used" cost — a real
  lever if the prompt were ever trimmed.
