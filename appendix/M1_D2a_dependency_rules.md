# M1 · D2(a) — Dependency Rules & What May Run in Parallel

## The single rule

> Two tool calls may share ONE turn **only if neither needs the other's
> output.** If call B's arguments come from call A's return value, they
> MUST be in different turns, in order.

The agent loop (`agent.py`) already enforces this mechanically: a turn
carries a list of `calls`, all executed, all observations appended
together. Packing a dependent call into the same turn as its parent
simply cannot work, because the parent's return is not available yet.

## Problem-A data-flow (which facts come from where)

```
get_claim  ──► {member_id, hospital_id, date_of_service, lines[...]}
                │
                ├─► lookup_policy(member_id)        ──► policy status/dates/headroom/exclusions
                ├─► lookup_hospital(hospital_id)    ──► panel status (record-only)
                ├─► check_coverage(code_i, policy_id) per line  ──► requires_preauth?, excluded?
                └─► check_duplicate_claim(member, hospital, dos, lines)  ── all from the claim
                          │
                check_coverage returns requires_preauth=True for line i
                          │
                          └─► get_preauthorisation(member, code_i, dos)   ← DEPENDS on coverage output
```

## The turn plan (this is the D2(c) win)

| Turn | Calls that run together | Why they can share the turn |
|------|------------------------|-----------------------------|
| 1 | `get_claim` | Alone. Every other call's arguments come from this return. |
| 2 | `lookup_policy` + `lookup_hospital` + `check_coverage` ×(one per line) + `check_duplicate_claim` | ALL of these take only fields from `get_claim`. Mutually independent → one turn. |
| 3 | `get_preauthorisation` (for each line where `requires_preauth` was True) | **Cannot** join turn 2: its arguments are decided by `check_coverage`'s output. This dependency is the ONLY thing that forces a later turn. |
| 4 | `issue_decision_letter` (gated) | Needs every disposition decided → last turn. |

## Pairs that MAY be parallelised (same turn, independent)
- `lookup_policy` ‖ `lookup_hospital`
- `lookup_policy` ‖ `check_coverage` (any line)
- `lookup_hospital` ‖ `check_coverage` (any line)
- `check_coverage` (line i) ‖ `check_coverage` (line j), i ≠ j
- `check_duplicate_claim` ‖ any of the above (it only needs claim fields)
- all of the above ‖ `lookup_hospital`

## Pairs that MUST stay sequential (different turns)
- `get_claim` → everything (turn 1 is mandatory alone)
- `check_coverage` → `get_preauthorisation` (the pre-auth arg is chosen from the coverage flag)
- anything → `issue_decision_letter` (it is the terminal gated action)
