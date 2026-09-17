#!/usr/bin/env python3
"""Run M3's Meta Llama battery with a checkpoint after every trial.

Usage: set OPENROUTER_API_KEY in the environment, then run this file from
A2_scaffold/. The committed config.py stays scripted by default. A malformed
live tool call is recorded as a failed trial so the remaining cases run.
"""

import contextlib
import io
import json
import os
from pathlib import Path
import traceback

import config
from harness import _is_negative, load_cases, load_key, report, run_set


MODEL = "meta-llama/llama-3.1-8b-instruct"
OUTPUT = Path(__file__).with_name("results_live_m3.json")


def save(payload):
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    os.replace(temporary, OUTPUT)


def main():
    config.BACKEND = "live"
    config.MODEL = MODEL
    # The model price used for the report's estimate; the provider's bill
    # may differ. API calls that crash before a record is returned are not
    # fully metered by this harness.
    config.PRICE_IN = 0.02
    config.PRICE_OUT = 0.04
    if not config.API_KEY:
        raise SystemExit("OPENROUTER_API_KEY is not set")

    cases = load_cases()
    key = load_key()
    payload = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {
        "config": (
            f"BACKEND=live  |  PROBLEM={config.PROBLEM}  |  model={MODEL}  |  "
            f"cap={config.MAX_TURNS} turns  |  autonomy={config.AUTONOMY}"
        ),
        "results": [], "judgement_queue": [], "summary": None,
    }
    if MODEL not in payload["config"]:
        raise SystemExit("Existing result file belongs to another model")
    results = payload["results"]
    queue = payload["judgement_queue"]
    completed = {(r["case_id"], r["trial"]) for r in results}
    total = sum(3 if _is_negative(key[cid]) else 1 for cid in cases)
    print(f"M3 live battery: {len(cases)} cases, {total} trials; "
          f"{len(completed)} already complete", flush=True)

    for cid in cases:
        count = 3 if _is_negative(key[cid]) else 1
        for trial in range(1, count + 1):
            if (cid, trial) in completed:
                continue
            try:
                trial_results, trial_queue = run_set([cid], trials_for=lambda _: 1)
                result = trial_results[0]
                result["trial"] = trial
                if trial == 1:
                    queue.append(trial_queue[0])
            except Exception as exc:
                result = {
                    "case_id": cid, "trial": trial, "passed": False,
                    "fails": [f"uncaught {type(exc).__name__}: {exc}"],
                    "family": key[cid].get("family"),
                    "record": {
                        "decision": None, "reason": str(exc), "case_id": cid,
                        "turns": 0, "cost_usd": 0,
                        "stopped_by": "uncaught_exception", "backend": "live",
                        "traceback": traceback.format_exc(),
                    },
                }
            results.append(result)
            save(payload)
            print(f"{len(results)}/{total} {cid} trial {trial}: "
                  f"{'PASS' if result['passed'] else 'FAIL'}", flush=True)

    with contextlib.redirect_stdout(io.StringIO()):
        payload["summary"] = report(results)
    save(payload)
    print("FINAL", payload["summary"], flush=True)


if __name__ == "__main__":
    main()
