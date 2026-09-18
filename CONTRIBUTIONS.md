# CONTRIBUTIONS

**Group 5 — NTU PE6201 Assessment 2 · Problem A (health-insurance claims triage agent)**

This document maps each member to the deliverables they owned and to the commits that
carry that work, so the commit history can be read directly against the brief's D0–D7
breakdown. It is built from two inputs: the agreed task split, and `git log` on `main`.

How to read it:

- The team worked in parallel on a single `main` branch, so the calendar ranges overlap.
  The **per-member commit list** below is the authoritative mapping.
- A few artefacts were handed to the group integrator and committed centrally on the
  author's behalf (the shared Colab workbench, the Windows-invalid-filename repair, the
  final report/documentation commit). Those commits are listed under *Team-wide /
  integration*; the underlying work is still credited to the member who produced it.

## At a glance

| Member | GitHub handle | Brief items | Module owned | Commit range |
|--------|---------------|-------------|--------------|--------------|
| M1 — Zhu Kai | `zkai023` | D1, D2(a), D2(c) | ReAct control loop; the 7-tool contract; single-turn parallel-vs-sequential measurement | `d1aad0c..d38e43b` (7) |
| M2 — Didaer | `didar.almrt` | D2(b), D3(a) | Six-field descriptor pack (v1 → v2); guardrail code layer | `5177934..f722661` (6) |
| M3 — Zhang Qiongwen | `qiongwenz748-odie` | D4, D5(a) | Evaluation-set framework; scripted reproducible harness; live battery | `b27bb1b..3344a3c` (5) |
| M4 — Li Jinting | `jintingli2004` | D3(b), D7 | Guardrail checklist (≥10 items, ≥3 hostile); two-failure reproduction | `05176fb..40dcf4b` (2) |
| M5 — Guo Shuhan | `nofear777tx` | D0(a)(b)(c) | "Why an agent" justification; the five D0(c) statements | `e240026..b1f03a1` (6) |
| M6 — Tang Yichen | `TyyCheN` | D6, §4, §6, video | Three-layer cost model; four levers & break-even; "what we would not deploy" | `d32f602..de62ea2` (14) |

## Per-member detail

### M1 — Zhu Kai (`zkai023`) · D1, D2(a), D2(c)

Owns the single-agent ReAct loop, the seven-tool contract for Problem A, and the
single-turn multi-tool (parallel vs sequential) runner together with its measurement.
Primary files: `A2_scaffold/agent.py`, `A2_scaffold/agent_sequential.py`,
`A2_scaffold/run_d2c.py`, `A2_scaffold/tools.py` (tool set), `A2_scaffold/config.py`.

- `d1aad0c` — scaffold and reference-data baseline (the shared tool layer)
- `7010505` — fix live agent loop (usage / timeout / parser); D2(a) tool contract; D2(c) parallel-vs-sequential runner
- `0daf894`, `bc4d9f2` — M1 live run record
- `eeccadb` — update code
- `e782ba3` — adapt agent to non-OpenAI models (response normalisation)
- `d38e43b` — submit M1 live results; rename M3 result file

### M2 — Didaer (`didar.almrt`) · D2(b), D3(a)

Owns the six-field descriptor pack (the D2(b) rewrite, v1 → v2) and the guardrail code
layer (turn / budget / duplicate / autonomy gate).
Primary files: `A2_scaffold/tools.py` (descriptors), `A2_scaffold/prompt.py`,
`A2_scaffold/guardrails.py`. M2's contributed evaluation cases are merged into
`A2_reference_data/data_A/claims.json` and `A2_scaffold/backends.py` (SCRIPTS).

- `5177934` — initial repository commit
- `6059408` — add case inputs
- `2d6e278`, `0d68428` — upload the six-field descriptor pack (Problem A v2)
- `4d1a5a0`, `f722661` — create then merge M2's contributed cases into `A2_reference_data/data_A` and `A2_scaffold/backends.py` (SCRIPTS)

> **Live-battery contribution (M2 — Didaer).** M2's live evaluation on
> `meta-llama/llama-3.1-8b-instruct` (descriptor v1 ↔ v2 comparison) has already been
> completed. She will commit the result file (`results_live_M2_*.json`) herself; this work
> is credited to M2 as her live-battery contribution even though the commit lands after the
> integration commit.

### M3 — Zhang Qiongwen (`qiongwenz748-odie`) · D4, D5(a)

Owns the evaluation-set framework, the scripted reproducible harness, and the
vendor-neutral backend replay used by the live battery.
Primary files: `A2_scaffold/harness.py`, `A2_scaffold/run_eval.py`,
`A2_scaffold/backends.py` (SCRIPTS), `A2_reference_data/check_my_data.py`.

- `b27bb1b` — make scripted decision reasons auditable
- `9f9a4a5` — evidence-based Section 3 draft
- `1bb6692`, `1cacee5` — Meta-Llama live evaluation results and measurement report
- `3344a3c` — checkpointed live evaluation runner

### M4 — Li Jinting (`jintingli2004`) · D3(b), D7

Owns the guardrail checklist (≥10 items, ≥3 hostile) and the two-failure reproduction
(runaway loop, duplicate-action loop).
Primary files: `A2_scaffold/guardrails.py` (`check_turns` / `check_duplicate`),
`appendix/M4_guardrail_test.py`, `appendix/M4_D3b_guardrail_checklist.md`,
`appendix/M4_D7_failures.md`.

- `05176fb` — guardrail checklist + failure reproductions
- `40dcf4b` — M4 live results (Qwen)

### M5 — Guo Shuhan (`nofear777tx`) · D0(a)(b)(c)

Owns the "why an agent at all" justification and the five D0(c) statements.
Primary files: `M5_Cases/`, `appendix/M5_*`, report §1.

- `e240026` — add case inputs
- `91fee68`, `36b524a` — `M5_Cases`
- `56187b8` — update M5 `claims.json`
- `5d4b4de` — update M5 `expected_outcomes_A.json`
- `b1f03a1` — M5 live results (DeepSeek)

### M6 — Tang Yichen (`TyyCheN`) · D6, §4, §6, video

Owns the three-layer cost model, the four levers and break-even analysis, and the
"what we would not deploy" section.
Primary files: `M6_Cases/`, cost notebook, `appendix/M6_*`.

- `d32f602`, `de62ea2` — `M6_Cases`
- `13c9724`, `fc9baf9`, `826523e`, `126373b` — claim narratives and expected-outcome notes
- `de4f837` — force JSON per vendor + live-backend JSON repair; per-model prices
- `b1ba85a`, `2c8b568`, `410bbbf`, `4fc274b` — live battery notebook (current slugs, prices)
- `7068517` — add case inputs
- `bac8038` — live results (anthropic/claude-haiku-4.5, v2 prompt)

## Team-wide / integration commits

These were pushed through the M1 handle on behalf of the group; the underlying work is
credited across the team as noted.

- `688eda5`, `3c8ff63`, `c6dd052` — shared Colab workbench notebook (all members)
- `fb4e6d2`, `517be02`, `da5e92e`, `8735a1c` — shared live-battery notebook (all members)
- `696e9fa`, `3c6ca52` — Windows-invalid-filename repair (M4 result file, content unchanged); fixed centrally
- `eccca15` — backfill 8 missing scripted cases in `backends.py` (case content contributed by M1–M6)
- `09af7ad` — `.gitignore` for locally generated results
- `99e8172` — team report, `SELF_ASSESSMENT.md`, `README.md`, this file
- merges — `33b7bdd`, `720ee28`, `4842733`

## Evaluation cases and live battery

Each member contributed a share of the 48 Problem-A evaluation cases (≈8 each), merged
into `A2_scaffold/backends.py` (SCRIPTS), `A2_reference_data/data_A/claims.json` and
`expected_outcomes_A.json`. Each member then evaluated one live model over the battery:

| Member | Live model |
|--------|------------|
| M1 | `openai/gpt-4o-mini` |
| M2 | `meta-llama/llama-3.1-8b-instruct` (descriptor v1 ↔ v2 comparison) |
| M3 | `meta-llama/llama-3.1-8b-instruct` |
| M4 | `qwen/qwen-2.5-7b-instruct` |
| M5 | `deepseek/deepseek-chat` |
| M6 | `anthropic/claude-haiku-4.5` |

## Handle → member mapping

| Member | Handle(s) |
|--------|-----------|
| M1 — Zhu Kai | `zkai023` |
| M2 — Didaer | `didar.almrt`, `didaralmrt-sudo` (repository owner) |
| M3 — Zhang Qiongwen | `qiongwenz748-odie` |
| M4 — Li Jinting | `jintingli2004` |
| M5 — Guo Shuhan | `nofear777tx` |
| M6 — Tang Yichen | `TyyCheN` |

## Commit convention

Every change is scoped to one module and named for its brief item (e.g. `M3: …`,
`M6: …`), so a reviewer can map each commit to a deliverable. When a commit also touches
another member's artefact, the message says so — e.g. `d38e43b` "submit M1 live results;
rename M3 result file".
