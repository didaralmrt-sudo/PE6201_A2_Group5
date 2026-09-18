# CONTRIBUTIONS

**Group 5 — NTU PE6201 Assessment 2 · Problem A (health-insurance claims triage agent)**

This document maps every member to the deliverables they owned and to the commits that
carry that work, so the commit history can be read directly against the brief's D0–D7
breakdown. It is built from two inputs: the agreed task split, and `git log` on `main`.

## How to read it

- The team worked in parallel on a single `main` branch, so **calendar commit ranges
  overlap**. The **per-member commit list** below is the authoritative mapping.
- **Evaluation cases (D4) were authored by each member individually.** Most members do
  not use a Git client, so case files were handed to the group integrator (M1) and
  committed centrally. Those commits therefore sit under the M1 handle (`zkai023`),
  **but every case is credited here to the member who wrote it** — see
  *Evaluation cases (D4)*. Where a member committed their own case material (M5, M6),
  those commits are listed under their own name as well.
- The same applies to other artefacts committed on a member's behalf (the shared Colab
  workbench, the Windows-invalid-filename repair, the final documentation commit) — those
  are listed under *Team-wide / integration*.
- **Every deliverable is referenced by its path inside the submitted tree**
  (`A2_scaffold/`, `A2_reference_data/`, `appendix/`, `video/`, root documents). Per-member
  case *working folders* (`M5_Cases/`, `M6_Cases/`) were drafting areas and are **not part
  of the submission**; the cases themselves live in the submitted shared data layer —
  `A2_reference_data/data_A/claims.json`, `A2_reference_data/expected_outcomes_A.json` and
  `A2_scaffold/backends.py` (`SCRIPTS`).
- The 48-case battery = **40 member-authored D4 cases + 8 teacher-shipped base cases**
  (e.g. `CLM-8710`, `REF-5602`). Only the 40 are attributed to members below.

## At a glance

| Member | GitHub handle | Brief items | Module owned | Submitted artefacts | Commits |
|--------|---------------|-------------|--------------|---------------------|---------|
| M1 — Zhu Kai | `zkai023` | D1, D2(a), D2(c) | ReAct control loop; the 7-tool contract; parallel-vs-sequential measurement; 7 D4 cases | `agent.py`, `agent_sequential.py`, `run_d2c.py`, `tools.py` (tool set), `backends.py` (case wiring), `config.py`, `appendix/M1_*` (5), 2 shared notebooks, `results_live_M1_*` | `d1aad0c..d38e43b` (7) |
| M2 — Didaer | `didar.almrt` | D2(b), D3(a) | Six-field descriptor pack (v1 → v2); system-prompt assembly; guardrail code layer; 7 D4 cases | `tools.py` (DESCRIPTORS), `prompt.py`, `guardrails.py`, `appendix/M2_v1_v2.md`, `TEAM_DECLARATION.pdf`, `results_live_M2_*` | `5177934..2cb9d1c` (7) |
| M3 — Zhang Qiongwen | `qiongwenz748-odie` | D4, D5(a) | Evaluation-set framework; scripted reproducible harness; live battery runner; 7 D4 cases | `harness.py`, `run_eval.py`, `backends.py` (SCRIPTS engine), `run_live_m3.py`, `check_my_data.py`, `appendix/M3_section3_evidence.md`, `results_live_M3_*` | `b27bb1b..3344a3c` (5) |
| M4 — Li Jinting | `jintingli2004` | D3(b), D7 | Guardrail checklist (≥10 items, ≥3 hostile); two-failure reproduction; 7 D4 cases | `guardrails.py` (D3(b) checks), `appendix/M4_guardrail_test.py`, `appendix/M4_D3b_guardrail_checklist.md`, `appendix/M4_D7_failures.md`, `results_live_M4_*` | `05176fb..40dcf4b` (2) |
| M5 — Guo Shuhan | `nofear777tx` | D0(a)(b)(c) | "Why an agent at all" justification; the five D0(c) statements; 6 D4 cases | `A2_reference_data/data_A/claims.json`, `A2_reference_data/expected_outcomes_A.json`, `TEAM_REPORT.md` §1, `results_live_M5_*` | `e240026..b1f03a1` (6) |
| M6 — Tang Yichen | `TyyCheN` | D6, §4, §6, video | Three-layer cost model; four levers & break-even; "what we would not deploy"; live-battery notebook; 6 D4 cases | `backends.py`, `config.py` (pricing, JSON repair), `A2_live_battery.ipynb`, `A2_reference_data/data_A/claims.json`, `make_fixtures_A.py`, `expected_outcomes_A.json`, `TEAM_REPORT.md` §4 & §6, `video/`, `results_live_M6_*` | `d32f602..bac8038` (14) |

## Per-member detail

### M1 — Zhu Kai (`zkai023`) · D1, D2(a), D2(c)

Owns the single-agent ReAct loop, the seven-tool contract for Problem A, and the
single-turn multi-tool (parallel vs sequential) runner together with its measurement.
Acted as group integrator: committed on behalf of members without a Git client, repaired
the Windows-invalid filename in the M4 result file, and backfilled the eight scripted
cases that were missing from `backends.py`.

Submitted files: `A2_scaffold/agent.py`, `A2_scaffold/agent_sequential.py`,
`A2_scaffold/run_d2c.py`, `A2_scaffold/tools.py` (tool set + call layer),
`A2_scaffold/backends.py` (scripted case wiring), `A2_scaffold/config.py`,
`A2_scaffold/demo_loop_failure.py`, `appendix/M1_D2a_dependency_rules.md`,
`appendix/M1_D2a_three_question_table.md`, `appendix/M1_D2c_sequential_vs_parallel.md`,
`appendix/M1_report_section2_tool_layer.md`, `appendix/M1_live_run_record.md`,
`A2_Team_Collaborative_Workbench.ipynb`, `A2_live_battery.ipynb`,
`A2_scaffold/results_live_M1_gpt-4o-mini.json`.

- `d1aad0c` — scaffold and reference-data baseline (the shared tool layer)
- `7010505` — fix live agent loop (usage / timeout / parser); D2(a) tool contract; D2(c) parallel-vs-sequential runner + dependency-rules appendix
- `0daf894`, `bc4d9f2` — M1 live run record
- `eeccadb` — case wiring into `claims.json`, `expected_outcomes_A.json`, `make_fixtures_A.py`
- `e782ba3` — adapt agent to non-OpenAI models (response normalisation)
- `d38e43b` — submit M1 live results; rename M3 result file to the convention

> **Evaluation cases (D4, authored by M1).** `CLM-8842`, `CLM-8850`, `CLM-8960`,
> `CLM-8861`, `CLM-8910`, `CLM-8888`, `CLM-8933` (7 cases). Authored in M1's working
> case set and merged into `A2_reference_data/data_A/claims.json`,
> `A2_reference_data/expected_outcomes_A.json` and `A2_scaffold/backends.py` (SCRIPTS).

### M2 — Didaer (`didar.almrt`) · D2(b), D3(a)

Owns the six-field descriptor pack — the D2(b) rewrite that takes the tool descriptions
from the verbose v1 form to the size-bounded v2 form — the system-prompt assembly that
renders those descriptors, and the guardrail code layer (turn / budget / duplicate /
autonomy gates).

Submitted files: `A2_scaffold/tools.py` (`DESCRIPTORS`), `A2_scaffold/prompt.py`,
`A2_scaffold/guardrails.py`, `appendix/M2_v1_v2.md`, `TEAM_DECLARATION.pdf`,
`A2_scaffold/results_live_M2_meta-llama(1).json`.

- `5177934` — initial repository commit (README)
- `6059408` — `TEAM_DECLARATION.pdf` (signed team declaration)
- `2d6e278`, `0d68428` — upload the six-field descriptor pack and the rewritten `prompt.py`; `appendix/M2_v1_v2.md` (the v1 ↔ v2 descriptor study)
- `4d1a5a0`, `f722661` — create then merge M2's contributed cases into `A2_reference_data/data_A/claims.json`, `A2_reference_data/expected_outcomes_A.json` and `A2_scaffold/backends.py` (SCRIPTS)
- `2cb9d1c` — commit M2's live-battery result file

> **Evaluation cases (D4, authored by M2).** `M2-CLM-9101` … `M2-CLM-9107` (7 cases).
> These were handed to the integrator and committed centrally, but are credited to M2.

> **Live-battery contribution (M2 — Didaer).** M2 ran the full 108-trial live battery on
> `meta-llama/llama-3.1-8b-instruct` and committed the result file herself
> (`A2_scaffold/results_live_M2_meta-llama(1).json`): 108 trials, 15 passed, **13.9%**.
> This is the vendor-neutral counterpart to her own v1 ↔ v2 descriptor study and is
> credited to M2 as her live-battery contribution.

### M3 — Zhang Qiongwen (`qiongwenz748-odie`) · D4, D5(a)

Owns the evaluation-set framework, the scripted reproducible harness, and the
vendor-neutral backend replay used by the live battery.

Submitted files: `A2_scaffold/harness.py`, `A2_scaffold/run_eval.py`,
`A2_scaffold/backends.py` (the `SCRIPTS` replay engine), `A2_scaffold/run_live_m3.py`,
`A2_reference_data/check_my_data.py`, `appendix/M3_section3_evidence.md`,
`A2_scaffold/results_live_M3_meta-llama.json`.

- `b27bb1b` — make scripted decision reasons auditable (the `SCRIPTS` engine in `backends.py`)
- `9f9a4a5` — evidence-based Section 3 draft
- `1bb6692` — Meta-Llama live evaluation results
- `1cacee5` — report the measured Meta-Llama live battery in `appendix/M3_section3_evidence.md`
- `3344a3c` — checkpointed live evaluation runner (`run_live_m3.py`)

> **Evaluation cases (D4, authored by M3).** `M3-CLM-9201` … `M3-CLM-9207` (7 cases).
> Handed to the integrator and committed centrally; credited to M3.

### M4 — Li Jinting (`jintingli2004`) · D3(b), D7

Owns the guardrail checklist (≥10 items, ≥3 hostile) and the two-failure reproduction
(runaway loop, duplicate-action loop), including the executable check script.

Submitted files: `appendix/M4_D3b_guardrail_checklist.md`,
`appendix/M4_D7_failures.md`, `appendix/M4_guardrail_test.py`,
`A2_scaffold/guardrails.py` (the `check_turns` / `check_duplicate` checks the checklist
specifies), `A2_scaffold/results_live_M4_qwen-qwen-2.5-7b-instruct.json`.

- `05176fb` — guardrail checklist + failure reproductions + executable guardrail test
- `40dcf4b` — M4 live results (Qwen)

> **Evaluation cases (D4, authored by M4).** `M4-CLM-9301` … `M4-CLM-9307` (7 cases).
> Handed to the integrator and committed centrally; credited to M4.

### M5 — Guo Shuhan (`nofear777tx`) · D0(a)(b)(c)

Owns the "why an agent at all" justification and the five D0(c) statements, written
straight into the team report and backed by the case material M5 authored.

Submitted files: `TEAM_REPORT.md` §1, `A2_reference_data/data_A/claims.json`,
`A2_reference_data/expected_outcomes_A.json`,
`A2_scaffold/results_live_M5_Deepseek_chat.json`.

- `e240026` — case inputs (initial hand-over of the M5 case pack)
- `36b524a` — `M5_Cases/M5_CLAIMS.json`, `M5_D4_cases.md`, `M5_KEYS.json` (working drafts of the six cases)
- `56187b8` — merge M5's claims into the shared `A2_reference_data/data_A/claims.json`
- `5d4b4de` — merge M5's expected outcomes into `A2_reference_data/expected_outcomes_A.json`
- `b1f03a1` — M5 live results (DeepSeek)

> **Evaluation cases (D4, authored by M5).** `M5-CLM-9001` … `M5-CLM-9006` (6 cases).
> Committed by M5 into the shared data layer under M5's own handle
> (`A2_reference_data/data_A/claims.json`, `A2_reference_data/expected_outcomes_A.json`),
> and replayed through `A2_scaffold/backends.py` (SCRIPTS). The per-member working folder
> `M5_Cases/` is a drafting area only and is not part of the submission.

### M6 — Tang Yichen (`TyyCheN`) · D6, §4, §6, video

Owns the three-layer cost model, the four levers and break-even analysis, and the
"what we would not deploy" section — and, in addition, much of the live-battery
infrastructure: per-model pricing, JSON repair for non-OpenAI vendors, the shared
Colab notebook, and the claim narratives.

Submitted files: `A2_scaffold/backends.py`, `A2_scaffold/config.py` (model prices, JSON
handling), `A2_live_battery.ipynb`, `A2_reference_data/data_A/claims.json`,
`A2_reference_data/make_fixtures_A.py`, `A2_reference_data/expected_outcomes_A.json`,
`TEAM_REPORT.md` §4 & §6, `video/README.md`,
`A2_scaffold/results_live_M6_claude-haiku-4.5.json`.

- `d32f602`, `de62ea2` — M6 case pack (`M6_CLAIMS.json`, `M6_D4_cases.md`, `M6_KEYS.json`) — working drafts
- `7068517` — case inputs
- `13c9724` — claim narratives added to `A2_reference_data/data_A/claims.json`
- `fc9baf9` — narrative fixtures in `A2_reference_data/make_fixtures_A.py`
- `826523e` — detailed notes in `A2_reference_data/expected_outcomes_A.json`
- `126373b` — refactor the M6 case scripts in `A2_scaffold/backends.py`
- `de4f837` — force JSON per vendor + JSON repair in the live backend; per-model prices
- `b1ba85a`, `410bbbf`, `4fc274b` — `A2_live_battery.ipynb`: current model slugs, deepseek in the model list, reset to latest `main`
- `2c8b568` — add the `deepseek/deepseek-chat` price to `A2_scaffold/config.py`
- `bac8038` — live results (`anthropic/claude-haiku-4.5`, v2 prompt) — **highest pass rate in the group, 91.7%**
- `9b53682` — housekeeping: remove the M6 working case folder

> **Evaluation cases (D4, authored by M6).** `M6-CLM-9401` … `M6-CLM-9406` (6 cases).
> Committed by M6 into the shared data layer (`A2_reference_data/data_A/claims.json`,
> `A2_reference_data/expected_outcomes_A.json`) and replayed through
> `A2_scaffold/backends.py` (SCRIPTS). The per-member working folder `M6_Cases/` is a
> drafting area only and is not part of the submission.

## Where each deliverable lives in the submission

Every row below is a file that ships in the final submission. Nothing depends on a
per-member working folder.

| Brief item | Deliverable | Submitted file(s) | Owner |
|-----------|-------------|-------------------|-------|
| D0(a)(b)(c) | "Why an agent" justification + five statements | `TEAM_REPORT.md` §1 | M5 |
| D1 | ReAct control loop | `A2_scaffold/agent.py` | M1 |
| D2(a) | Seven-tool contract | `A2_scaffold/tools.py`, `appendix/M1_D2a_*.md` | M1 |
| D2(b) | Six-field descriptors (v1 → v2) | `A2_scaffold/tools.py` (`DESCRIPTORS`), `A2_scaffold/prompt.py`, `appendix/M2_v1_v2.md` | M2 |
| D2(c) | Parallel vs sequential single turn | `A2_scaffold/agent_sequential.py`, `A2_scaffold/run_d2c.py`, `appendix/M1_D2c_sequential_vs_parallel.md` | M1 |
| D3(a) | Guardrail code layer | `A2_scaffold/guardrails.py` | M2 |
| D3(b) | Guardrail checklist (≥10 items, ≥3 hostile) | `appendix/M4_D3b_guardrail_checklist.md`, `appendix/M4_guardrail_test.py` | M4 |
| D4 | Evaluation set (40 member-authored cases) | `A2_reference_data/data_A/claims.json`, `A2_reference_data/expected_outcomes_A.json`, `A2_scaffold/backends.py` | M1–M6 (see table) |
| D5(a) | Scripted reproducible harness | `A2_scaffold/harness.py`, `A2_scaffold/run_eval.py`, `A2_reference_data/check_my_data.py` | M3 |
| D5(a) | Live battery runner | `A2_scaffold/run_live_m3.py`, `A2_live_battery.ipynb` | M3, M6 |
| D6 | Three-layer cost model, levers, break-even | `TEAM_REPORT.md` §4; per-model prices in `A2_scaffold/config.py` | M6 |
| D7 | Two-failure reproduction | `appendix/M4_D7_failures.md`, `A2_scaffold/demo_loop_failure.py` | M4, M1 |
| §2 | Tool layer write-up | `TEAM_REPORT.md` §2, `appendix/M1_report_section2_tool_layer.md` | M1 + M2 |
| §3 | Evidence write-up | `TEAM_REPORT.md` §3, `appendix/M3_section3_evidence.md` | M3 |
| §5 | Two failures write-up | `TEAM_REPORT.md` §5 | M4 |
| §6 | What we would not deploy | `TEAM_REPORT.md` §6 | M6 |
| — | Team declaration | `TEAM_DECLARATION.pdf` | M2 |
| — | Live battery results | `A2_scaffold/results_live_M1_*.json` … `results_live_M6_*.json` | M1–M6 |
| — | Demo video | `video/` | M6 |

## Team-wide / integration commits

These were pushed through the M1 handle on behalf of the group; the underlying work is
credited across the team as noted.

- `688eda5`, `3c8ff63`, `c6dd052` — shared Colab workbench notebook `A2_Team_Collaborative_Workbench.ipynb` (all members)
- `fb4e6d2`, `517be02`, `da5e92e`, `8735a1c` — shared live-battery notebook `A2_live_battery.ipynb` (all members; M6 also commits to it directly)
- `696e9fa`, `3c6ca52` — Windows-invalid-filename repair (M4 result file, content unchanged); fixed centrally
- `eccca15` — backfill 8 missing scripted cases in `backends.py` (case content contributed by M1–M6)
- `09af7ad` — `.gitignore` for locally generated results
- `99e8172` — team report, `SELF_ASSESSMENT.md`, `README.md`, this file, appendix filename cleanup
- `f864bef` — final documentation commit
- merges — `33b7bdd`, `720ee28`, `4842733`, `3a9618e`

## Evaluation cases and live battery

The battery holds 48 Problem-A cases. Of these, **40 were authored by the six members
as their D4 deliverable** and merged into `A2_reference_data/data_A/claims.json`,
`A2_reference_data/expected_outcomes_A.json` and `A2_scaffold/backends.py` (SCRIPTS);
the remaining 8 are teacher-shipped base cases. Per-member allocation (each credited to
its author even where committed centrally by the integrator):

| Member | D4 evaluation cases | Count |
|--------|---------------------|-------|
| M1 — Zhu Kai | `CLM-8842`, `CLM-8850`, `CLM-8960`, `CLM-8861`, `CLM-8910`, `CLM-8888`, `CLM-8933` | 7 |
| M2 — Didaer | `M2-CLM-9101` … `M2-CLM-9107` | 7 |
| M3 — Zhang Qiongwen | `M3-CLM-9201` … `M3-CLM-9207` | 7 |
| M4 — Li Jinting | `M4-CLM-9301` … `M4-CLM-9307` | 7 |
| M5 — Guo Shuhan | `M5-CLM-9001` … `M5-CLM-9006` | 6 |
| M6 — Tang Yichen | `M6-CLM-9401` … `M6-CLM-9406` | 6 |
| **Total member-authored** | | **40** |

Each member then evaluated one live model over the battery. Pass rates below are read
directly from their committed `results_live_*.json` files.

| Member | Live model | Trials | Passed | Pass rate |
|--------|------------|--------|--------|-----------|
| M1 | `openai/gpt-4o-mini` | 33 | 8 | 24.2% |
| M2 | `meta-llama/llama-3.1-8b-instruct` (with the v1 ↔ v2 descriptor study) | 108 | 15 | 13.9% |
| M3 | `meta-llama/llama-3.1-8b-instruct` | 108 | 5 | 4.6% |
| M4 | `qwen/qwen-2.5-7b-instruct` | 108 | 44 | 40.7% |
| M5 | `deepseek/deepseek-chat` | 108 | 85 | 78.7% |
| M6 | `anthropic/claude-haiku-4.5` | 108 | 99 | **91.7%** |
| **Reference** | scripted replay (no model, no key, no network) | 108 | 108 | **100%** |

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
