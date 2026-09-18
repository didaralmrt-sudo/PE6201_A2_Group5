# D6 · Cost model — Problem A

All figures below are actual token counts taken from live batteries and priced at list price. No extrapolation from a single run.

## Assumptions, stated

| Assumption       | Value                                                      | Where it comes from                   |
| ---------------- | ---------------------------------------------------------- | ------------------------------------- |
| Volume           | 8,000 claims / month                                       | Appendix A, Problem A                 |
| Failure cost `F` | US$7.60 per misrouted claim                                | a claims assessor at US$38/h × 12 min |
| Battery          | 48 cases = 18 act × 1 trial + 30 negative × 3 = 108 trials | D4                                    |
| Prompt           | v2, identical for every model                              | D2(b)                                 |
| Caps in force    | 8 turns · 60,000 tokens / run · autonomy `confirm`         | D3                                    |
| Pricing          | OpenRouter list, no caching, no reasoning mode             | `config.MODEL_PRICES`                 |

Which cost world are we in. A wrong outcome here goes to a person, not back into the loop. So we add (1 − p) × F instead of dividing by the success rate. Dividing by p prices retry until it works, and that is not what happens to a misrouted claim.

## The three layers

```
layer 1  inference     tokens × list price          per run
layer 2  remediation   (1 − p) × US$7.60            per claim
layer 3  fixed         logging, storage, monthly regression run
```

Layer 3 is the same for any model we pick, so it just moves every column below it down the same amount and makes no comparisons. We have the machine part costing at US\$150/month (8,000 records with decision-record storage and log retention, with one scripted battery and one live battery per month for regression check).  We do not cost engineer time to work through the judgment queue. It is real, and is probably the largest fixed item, we have no defensible rate for it, so we leave it named and unpriced rather than invented.

## The ledger

Five models, one per member, all on the same 108 trials and the same v2 prompt.

| Model                                | Tier  | Pass rate          | Layer 1 / run | Layer 2 / claim | All-in / claim | Monthly @ 8,000 |
| ------------------------------------ | ----- | ------------------:| -------------:| ---------------:| --------------:| ---------------:|
| `anthropic/claude-haiku-4.5`         | mid   | **91.7%** (99/108) | $0.015062     | $0.6333         | **$0.6484**    | **$5,187**      |
| `deepseek/deepseek-chat`             | cheap | 78.7% (85/108)     | $0.002806     | $1.6185         | $1.6213        | $12,971         |
| `openai/gpt-4o-mini`                 | cheap | 74.1% (80/108)     | $0.001394     | $1.9704         | $1.9718        | $15,774         |
| `qwen/qwen-2.5-7b-instruct`          | cheap | 40.7% (44/108)     | $0.001037     | $4.5037         | $4.5047        | $36,038         |
| `meta-llama/llama-3.1-8b`            | cheap | 19.4% (21/108)     | $0.000175     | $6.1222         | $6.1224        | $48,979         |
| *no agent — every claim to a person* | —     | —                  | —             | $7.60           | $7.60          | $60,800         |

Two things to glean from this table.  

The mid-tier model costs 86× the run cost of the cheapest model and remains the cheapest column on the page, less than half the all-in cost of DeepSeek. For haiku, layer 2 is layer 1 × 42.  

The all-in rank is the exact reverse of the accuracy rank. Sort the five models by price per token and you get a different order. Sort by all-in cost and you get the accuracy order every time. Across an 86× spread in token price, price never once reorders the table. That is the whole argument for spending on accuracy, in one observation.

## The four levers

| Lever                                                        | What we measured                       | Before → after                                                                        |
| ------------------------------------------------------------ | -------------------------------------- | ------------------------------------------------------------------------------------- |
| **1 · Tool block `B`** — re-sent every turn, linear in `T`   | prompt + descriptor text actually sent | v1 **1,233** → v2 **1,684** tokens (+37%)                                             |
| **2 · Turn count `T`** — the term we can actually cut        | D2(c), 7 cases sequential vs parallel  | **43 → 22 turns (−49%)**, input **322,800 → 127,200 (−61%)**, pass rate unchanged 7/7 |
| **3 · Observation size `D`** — compounds on every later turn | input tokens per turn, by turn count   | **5,192 / 4,311 / 3,830 / 3,849 / 3,899** for 1/2/4/5/6-turn runs                     |
| **4 · Success rate**                                         | the ledger above                       | v1 **15.7%** → v2 **91.7%** on haiku                                                  |

Which was dominant, and how do we know.

Across the whole bill: lever 4, by a long way. On our model of choice, layer 2 is 42× layer 1, and it is the only layer that moves when accuracy moves. Every other lever is fighting for its share of \$0.015; this one moves \$7.60.

Lever 1 × lever 2, not lever 3, in layer 1. The best fit for the haiku runs is `input ≈ 3,552 × T + 1,537` — linear in turn count, not quadratic. The input per turn is flat, and even slightly decreases as runs get longer (5,192 → 3,899). This is the signature of a fat re-sent prefix and thin observations.  
So we pay for the tool block `B` on every turn, and `T` is the multiplier on it; the compounding term `D` never grows fast enough to bite. That is the opposite of the usual warning about quadratic growth of history, and we can only see it because we measured per-turn input instead of assuming the formula.  

We deliberately grew `B`. The v2 descriptor rewrite made the re-sent block 37% bigger, a flat loss on levers 1-3. It bought +76 points of haiku pass rate, worth $5.78/claim in layer 2, versus about $0.004/run in extra tokens. That trade is not close at `F` = \$7.60.  

We also see from the v1 pass that the fix is model dependent. The same prompt change measured on llama-3.1-8b moved it only 13.9% -> 19.4%, against 15.7% -> 91.7% on haiku. Lever 4 is not a property of the prompt, it is a property of the prompt and the model.

## Sensitivity

Accuracy is the dominant lever, so we vary it, ±10 points around the measured
91.7% with layer 1 held at its measured value:

| Pass rate            | All-in / claim | Monthly    |
| --------------------:| --------------:| ----------:|
| 81.7%                | $1.4084        | $11,267    |
| 86.7%                | $1.0284        | $8,227     |
| **91.7% (measured)** | **$0.6484**    | **$5,187** |
| 96.7%                | $0.2684        | $2,147     |

Each 5 points of accuracy is worth $0.38 per claim — $3,040 a month. A 10 point swing shifts the bill more than the entire inference spend of any model in the table. This conclusion holds for the whole range: haiku is the cheapest option in each row, because even at 81.7% the all-in cost (\$1.41) is lower than DeepSeek's measured \$1.62.

## Break-even

```
p* = 1 − (E − C) / F        E = $0.6484 (haiku all-in)   F = $7.60
```

A cheap model's inference saving is so small that `p*` is 91.5% for all four
of them. Measured against it:

| Model                       | Needs | Has   | Short by     |
| --------------------------- | -----:| -----:| ------------:|
| `deepseek/deepseek-chat`    | 91.5% | 78.7% | **12.8 pts** |
| `openai/gpt-4o-mini`        | 91.5% | 74.1% | 17.4 pts     |
| `qwen/qwen-2.5-7b-instruct` | 91.5% | 40.7% | 50.7 pts     |
| `meta-llama/llama-3.1-8b`   | 91.5% | 19.4% | 72.0 pts     |

DeepSeek, our best cheap model, is 78.7%, and would need to hit 91.5% to beat the mid-tier model on total cost, so it falls 12.8 points short (and we ship haiku, the token price we save is worth less than the claims we would misroute).  

This is a statement about `F`, not the models. At `F` = \$0.76 the break-even would be about 86% and the cheap model's 86× price advantage would count. The more expensive it is to be wrong, the less the price per token matters.

## Caching and reasoning models

Neither is in the figures priced. Prompt caching attacks precisely our dominant term, a 3,552-token prefix re-sent on every turn, so it is the first optimization worth testing; we did not price it because discounts and hit-rate rules differ per vendor and would have to be measured, not modeled. Reasoning mode was not used: it charges thinking to output, and output is 5× input on our model, so it would inflate the one layer that is already a rounding error while doing nothing for layer 2.

## The three caps that ship

| Cap                    | Value                                                   | Set from                                                                                                                                                 |
| ---------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Step cap               | **8 turns**                                             | worst legitimate run is 6 turns (108 scripted, 108 haiku); one turn of headroom, not a round number                                                      |
| Budget ceiling         | **60,000 tokens / run**                                 | worst legitimate run is 24,017 tokens; 2.5× headroom                                                                                                     |
| Monthly limit per user | **12 runs / member / month** (≈$0.18 at the haiku rate) | a policy choice, not a measurement — it bounds a looping integration or a repeatedly re-submitted claim; beyond it the member's claims queue to a person |

The first two are set from the measured turn distribution: no run in either battery hit either cap, so neither truncates honest work.


