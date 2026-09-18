# Self-Assessment — Group 5 (PE6201 A2, Problem A)

One row per member. Live pass rates are read directly from each member's
`results_live_*.json` (in `A2_scaffold/`); see `TEAM_REPORT.md` §3 for context.

| Member | Role (D-ranges) | Model (OpenRouter) | Trials | Passed | Pass rate (v2) | v1 pass | Cases authored | Result file |
|--------|-----------------|--------------------|--------|--------|----------------|---------|----------------|-------------|
| M1 | D1 / D2(a) / D2(c) | openai/gpt-4o-mini | 33 | 8 | **24.2%** | — (scripted baseline 100%) | 7 | `results_live_M1_gpt-4o-mini.json` |
| M2 | D2(b) / D3(a) | (v1/v2 to run on M3's Llama) | — | — | **pending** | **pending** | 7 | *(not yet committed)* |
| M3 | D4 / D5(a) | meta-llama/llama-3.1-8b-instruct | 108 | 5 | **4.6%** | — (scripted baseline 100%) | 7 (+33 set) | `results_live_M3_meta-llama.json` |
| M4 | D3(b) / D7 | qwen/qwen-2.5-7b-instruct | 108 | 44 | **40.7%** | — (scripted baseline 100%) | 7 | `results_live_M4_qwen-qwen-2.5-7b-instruct.json` |
| M5 | D0 | deepseek/deepseek-chat | 108 | 85 | **78.7%** | — (scripted baseline 100%) | 6 | `results_live_M5_Deepseek_chat.json` |
| M6 | D6 / §4 / §6 | anthropic/claude-haiku-4.5 | 108 | 99 | **91.7%** | — (scripted baseline 100%) | 6 | `results_live_M6_claude-haiku-4.5.json` |

**Scripted harness (all members, v2 prompt):** 48 cases, **108/108 trials, 100%
pass** — the number a clean clone must reproduce.

## Notes

- **Pass rate** = `summary.pass_rate` from each `results_live_*.json`. M1 ran 33
  trials (their own 7-case subset × 3); the other four ran the full 108-trial
  battery (48 cases, 3 trials on the negative families).
- **v1 pass** column: only M2's deliverable includes a measured v1↔v2 comparison
  (descriptor rewrite). M2's live v1/v2 run on M3's Llama model is **still to be
  done** — record it in `appendix/M2_v1_v2.md` and here once run. For the other
  members, "v1" equivalence is the scripted harness (100%), since they did not
  run a separate v1 prompt.
- **Where the models agree / break:** all six get the *decision* right far more
  often than the *trigger label*; the gap is wording (`lapsed` vs `policy_lapsed`,
  `date_of_service` vs `outside_policy_dates`). The cheapest model (llama-3.1-8b)
  and the most expensive (claude-haiku-4.5) bracket the range; cost per run
  scaled with tier and output tokens (llama ≈ US$0.015 → haiku ≈ US$1.63).
- **Action item:** M2 to produce `results_live_M2_*.json` (v1 and v2 on the same
  model) and fill the two pending cells above.
