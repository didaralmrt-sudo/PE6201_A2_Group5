# D6 · Cost model — Problem A

All measurements presented below are empirical. Pass rates refer to the D4 test set. Token counts and respective costs are computed using D5 live batteries at list price.

## Assumptions

| Assumption | Value | Source |
|---|---|---|
| Volume | 8,000 claims / month | Appendix A |
| Cost of one failure F | US\$7.60 | a claims assessor at US\$38/h for 12 minutes |
| Battery | 48 cases → 18 act × 1 trial + 30 negative × 3 = 108 trials | D4 |
| Prompt | v2, the same for every model | D2(b) |
| Caps | 8 turns · 60,000 tokens per run · autonomy confirm | D3 |

Which world we are in: a wrong claim goes to a person, and does not go back into the loop to be retried. So we add (1 − p) × F. We do not divide by the success rate.

## The three-layer structure

| Layer | What it is | Ours |
|---|---|---|
| 1 · Per-task variable | input + output tokens × price | \$0.015 per run on haiku |
| 2 · Per-task expected fallback | (1 − pass rate) × \$7.60 | \$0.633 per claim on haiku |
| 3 · Fixed monthly | storage, logging, monthly eval re-run | ≈ US\$150 / month |

Layer 3 is fixed in all the models under consideration and does not impact the model choice. No fee is involved for the engineer's time used for checking the judgment queue. It is real and probably the largest fixed item, but we have no defensible rate for it, so we name it and leave it unpriced.

## The ledger

Five models are considered, one per member, all tested on the same 108 trials with the same v2 prompt. The metric "cost per successful task" includes contributions from layer 1 and layer 2.

| Model | Tier | Pass rate | Layer 1 / run | Layer 2 / claim | Cost per successful task | Monthly @ 8,000 |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4.5 | mid | 91.7% (99/108) | \$0.0151 | \$0.633 | \$0.648 | \$5,187 |
| deepseek/deepseek-chat | cheap | 78.7% (85/108) | \$0.0028 | \$1.619 | \$1.621 | \$12,971 |
| openai/gpt-4o-mini | cheap | 74.1% (80/108) | \$0.0014 | \$1.970 | \$1.972 | \$15,774 |
| qwen/qwen-2.5-7b-instruct | cheap | 40.7% (44/108) | \$0.0010 | \$4.504 | \$4.505 | \$36,038 |
| meta-llama/llama-3.1-8b | cheap | 19.4% (21/108) | \$0.0002 | \$6.122 | \$6.122 | \$48,979 |
| *no agent — a person reads every claim* | — | — | — | \$7.60 | \$7.60 | \$60,800 |

### Two takeaways from the ledger

- The mid-tier model runs at 86 times the cost per run of the cheapest model, yet it is still the cheapest column on the page — less than half of DeepSeek. In the case of haiku, layer 2 costs 42 times as much as layer 1.
- Ordering models by price per token gives one ranking order; ordering by cost per successful task gives an accuracy-based one. Across the 86× disparity in token price, no price-based reordering occurs.

## The four levers

| Lever | Where we built it | Measured before → after |
|---|---|---|
| 1 · Tool block B | D2(a)/D2(b) | v1 1,561 → v2 2,327 tokens (+49%), re-sent every turn |
| 2 · Turn count T | D2(c) parallel calls | 43 → 22 turns (−49%); input 322,800 → 127,200 tokens (−61%); pass rate unchanged, 7/7 both ways |
| 3 · Observation size D | D2(b) return-shape rewrite | per call: lookup_policy 442 → 354 chars (−20%), check_duplicate_claim 214 → 164 (−23%), get_claim 395 → 420 (+6%, deliberate) |
| 4 · Success rate | D4 eval set | v1 13.9% → v2 19.4% on llama-3.1-8b, the one model we held fixed; 19.4%–91.7% across the five models on v2 |

### Identification of the dominating lever and arguments

Overall, Lever 4 dominates the cost composition everywhere. The costs of Layer 2 are 42 times larger than those of Layer 1 in the chosen model, and Layer 2 is the only layer whose cost moves when accuracy moves. The other three levers compete over about \$0.015 per run, whereas Lever 4 moves Layer 2, which is \$0.633 per claim on Haiku and climbs towards \$7.60 as accuracy falls.

In Layer 1, the dominating element is Lever 1, not Lever 3. As the brief warns, a large observation set compounds, whereas a large tool block grows linearly. In our case the compounding never showed up, and two facts show why:

- The observational data are limited. After the rewrite, a tool returns between 164 and 420 characters per call, meaning that each additional turn adds little history.
- The tool block is not small: 2,327 tokens, and it is re-sent every turn, regardless of whether a tool is used.

The evidence is the input tokens per turn. For each haiku run we divided its input tokens by its number of turns.

| Run length | 1 turn | 2 turns | 4 turns | 5 turns | 6 turns |
|---|---|---|---|---|---|
| Input tokens per turn | 5,192 | 4,311 | 3,830 | 3,849 | 3,899 |

In case of accumulating observations, one should see increasing values of the metric for longer runs. The metric does not: the figure stays flat and in fact falls slightly. That is what you see when the re-sent prefix is the bill and the observations are not.

Layer 1 was purposely raised. With the Version 2 rewrite, the re-sent block got a 49% increase and resulted in a direct loss on Layer 1. In order to find out how much benefit could be expected from this increase, the model was kept constant, while both prompts were evaluated on the llama-3.1-8b model: the metric went from 13.9% to 19.4% for a gain of 5.6 percentage points. It translates into the value of \$0.42 per claim on Layer 2. Even at the Haiku price level, the additional tokens amount to \$0.0013 per run. With F = \$7.60, the trade is not a close call: the gain outweighs the extra tokens by more than 300 times.

There is one more limitation. The 5.6 percentage point improvement has been measured on the 8B model, the worst in the evaluation set, and 19.4% is nowhere near deployable. We ran v1 on one model only, because a fair comparison requires changing one thing at a time. So we can say the rewrite was worth about 5.6 points, or \$0.42 a claim. We cannot say the same gain would appear on haiku.

## Sensitivity

Our pass rate is an estimate, so we show a range rather than one number: cost per successful task at ±10 percentage points around the measured 91.7%, with layer 1 held at its measured value.

| Pass rate | Cost per successful task | Monthly @ 8,000 |
|---|---|---|
| 81.7% | \$1.408 | \$11,267 |
| 86.7% | \$1.028 | \$8,227 |
| **91.7% (measured)** | **\$0.648** | **\$5,187** |
| 96.7% | \$0.268 | \$2,147 |

Every 5 points of accuracy is worth \$0.38 a claim, or \$3,040 a month. A 10-point swing moves the bill by more than the entire inference spend of any model in the table.

**Does the conclusion survive the range? Yes.** Even at the bottom of it, 81.7%, haiku costs \$1.41 per successful task — still below DeepSeek's measured \$1.62. Haiku is the cheapest option at every row.

## Break-even

```
break-even p* = 1 − (E − C) / F

C = what one run costs on the cheap model (tokens only)
E = cost per successful task on the expensive model = $0.6484
F = cost of one failure                             = $7.60
```

A cheap model saves so little per run that p* comes out at **91.5%** for all four of them.

| Cheap model | Needs | Measured | Short by |
|---|---|---|---|
| deepseek/deepseek-chat | 91.5% | 78.7% | 12.8 points |
| openai/gpt-4o-mini | 91.5% | 74.1% | 17.4 points |
| qwen/qwen-2.5-7b-instruct | 91.5% | 40.7% | 50.7 points |
| meta-llama/llama-3.1-8b | 91.5% | 19.4% | 72.0 points |

Our best cheap model, DeepSeek, scored 78.7% and would need 91.5% to beat the mid-tier model on total cost, so it is 12.8 points shy — and we ship haiku.

This is really a fact about F, not about the models. If a failure cost \$0.76 instead of \$7.60, the break-even would be about 86% and the cheap model's price advantage would start to matter. The higher the cost of being wrong, the less the price per token matters.

## Caching and reasoning models

**Prompt caching:** not used and not in the figures above. It attacks precisely our dominant term: a 2,327-token block re-sent every turn. That is the first thing we would test. We did not model it because the discount and hit-rate rules are different per vendor and would need to be measured to be worth quoting.

**Reasoning model:** none. Output is 5× input on our model, and thinking tokens are charged as output. This would bloat layer 1, which is already a rounding error, and do nothing for layer 2.

## The three caps that ship

Set from the measured turn distribution, not from round numbers.

| Cap | Value | Why this number |
|---|---|---|
| Step cap | 8 turns | the longest honest run is 6 turns; 8 leaves one turn of headroom |
| Budget ceiling | 60,000 tokens / run | the heaviest honest run is 33,120 tokens in + out; 1.8× headroom |
| Monthly limit per user | 12 runs / member / month (≈\$0.18) | a policy choice, not a measurement — it bounds a looping integration or a member re-submitting the same claim; past it, their claims go to a person |

No run in either battery hit either of the first two caps, so neither of them truncates honest work.
