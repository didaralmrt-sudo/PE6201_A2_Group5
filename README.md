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
  standard library** — there is nothing to `pip install`.
- **Live mode only**: an OpenRouter API key in the environment
  (`OPENROUTER_API_KEY`). Scripted mode (the default, and the one a clean clone
  must reproduce) needs no key and costs nothing.

```bash
# Linux / macOS
export OPENROUTER_API_KEY="sk-or-..."

# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-or-..."
```

---

## 2. Clone and run (a stranger's path)

```bash
git clone https://github.com/didaralmrt-sudo/PE6201_A2_Group5.git
cd PE6201_A2_Group5

# Reproduce the scripted evaluation set (default backend, no API key needed)
python A2_scaffold/run_eval.py
```

Expected output: the scripted backend replays fixed answers and the run ends at
**100% pass (48 cases, 108/108 trials)**. The scripted backend never reads the
prompt, so this number is stable on any machine.

> On Windows: do **not** create result-file names containing a colon (`:`) — it
> is a reserved character and will make the repo un-cloneable for other Windows
> users. Model names in result files use a hyphen instead, e.g.
> `results_live_M4_qwen-qwen-2.5-7b-instruct.json`.

---

## 3. Switching to live mode (costs money)

Edit `A2_scaffold/config.py`:

```python
BACKEND = "live"                       # "scripted" | "live"
MODEL   = "openai/gpt-4o-mini"         # any OpenRouter model id
```

Then run the same entry point; live calls hit OpenRouter and are billed to your
key. For running the whole battery (or letting the notebook manage the model),
use `A2_live_battery.ipynb` — its setup cell clones/pulls the latest scaffold
and runs every case for the chosen model.

Optional: point the data directory elsewhere with `A2_DATA=/path/to/data`.

---

## 4. Repository layout

```
A2_scaffold/            the agent: agent.py, tools.py, guardrails.py,
                        prompt.py, backends.py (SCRIPTS + replay),
                        harness.py, run_eval.py, config.py
A2_reference_data/      claims.json, expected_outcomes_A.json,
                        check_my_data.py, policies/hospitals/... fixtures
M5_Cases/  M6_Cases/   per-member case + key material
appendix/               per-member reports & evidence (M1–M6)
results_live_*.json    each member's live-battery run (on OpenRouter)
TEAM_REPORT.md          the six-section team report (≤2000 words)
SELF_ASSESSMENT.md      per-member model, pass rate, cases
CONTRIBUTIONS.md        member → module mapping
video/                  where the demo video is submitted (see video/README.md)
```

---

## 5. Key commands

| Goal | Command |
|------|---------|
| Reproduce scripted set (default) | `python A2_scaffold/run_eval.py` |
| Run everything that is scripted | `python A2_scaffold/run_eval.py --all` |
| Inspect the exact prompt + size | `python A2_scaffold/run_eval.py --prompt` |
| Check data consistency | `python A2_reference_data/check_my_data.py` |
| Run a single case (manual) | `python A2_scaffold/harness.py <CLM-ID>` |

---

## 6. Report & assessment

- **Team report** — `TEAM_REPORT.md` (§1 Why an Agent · §2 Tool Layer ·
  §3 Evidence · §4 Cost · §5 Two Failures · §6 What We Would Not Deploy).
- **Self-assessment** — `SELF_ASSESSMENT.md` (each member's model, live pass
  rate, case count).
- **Contributions** — `CONTRIBUTIONS.md`.
