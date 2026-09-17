"""
PE6201 · A2 scaffold — THE AGENT LOOP, SEQUENTIAL VARIANT  (D1 / D2(c))
====================================================================
This is the SAME hand-rolled ReAct loop as `agent.py`, with exactly ONE
behavioural change: in each tool-calling turn it executes ONLY THE FIRST
call of `move["calls"]` and then returns to the loop for the next move.
That forces one tool call per turn (a strictly sequential schedule).

`agent.py` (the shipped, default loop) may pack several independent calls
into one turn. This file is the counterpart used to produce the
"sequential" column of the D2(c) comparison: same evaluation set, same
prompts, same tools — only the call-scheduling differs.

Run it (scripted backend, free):
    python run_d2c.py            # or your own harness that imports this module

The numbers it produces are the "sequential" side of
`M1_D2c_sequential_vs_parallel.md`. Turns and pass-rate are exact and
reproducible; token/cost on the scripted backend are ESTIMATES.
"""
import json
import time

import config
import prompt
import tools
from backends import make_backend
from guardrails import Guardrails, GuardrailStop


def _normalize_calls(move):
    """Turn whatever shape a live model returned for `calls` into a list of
    (name, args) tuples, so the rest of the loop can unpack it safely.

    Real models do NOT all honour the requested `[["tool", {args}], ...]`
    shape. We have seen, and must survive, every one of these:
      - [["tool", {args}], ...]                 (the requested format)
      - [{"tool": "x", "args": {...}}, ...]
      - [{"name": "x", "arguments": "{...}"}]   (OpenAI tool_calls style)
      - {"tool": {args}, ...}                   (an object, not an array)
      - top-level "tool"/"args" keys            (a single call, no list)

    Anything we cannot make sense of is dropped - it never crashes the
    whole run. A model that emits a malformed call simply gets no tool
    executed for that step, which is the safe failure.
    """
    if not isinstance(move, dict):
        return []
    raw = move.get("calls")
    if not raw:
        t = move.get("tool")
        a = move.get("args", {})
        return [(t, a if isinstance(a, dict) else {})] if t else []
    if isinstance(raw, dict):
        return [(k, v if isinstance(v, dict) else {}) for k, v in raw.items()]
    if isinstance(raw, (list, tuple)):
        out = []
        for item in raw:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                out.append((item[0], item[1] if isinstance(item[1], dict) else {}))
            elif isinstance(item, dict):
                name = (item.get("tool") or item.get("name")
                        or (item.get("function") or {}).get("name"))
                args = item.get("args", item.get("arguments"))
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {}
                if name:
                    out.append((name, args if isinstance(args, dict) else {}))
            elif isinstance(item, str):
                out.append((item, {}))
        return out
    return []


def run_case(case_id, problem=None, approve=None, verbose=False):
    """Run ONE case from a clean state and return the decision record.

    SEQUENTIAL VARIANT: one tool call per turn (see module docstring).
    """
    problem = problem or config.PROBLEM
    started = time.time()

    guards = Guardrails(config.MAX_TURNS, config.MAX_TOKENS_PER_RUN,
                        config.AUTONOMY)
    backend = make_backend(
        case_id,
        tool_descriptors=[tools.DESCRIPTORS[n] for n in tools.REGISTRY[problem]
                          if n in tools.DESCRIPTORS],
        system_prompt=prompt.build_system_prompt(problem))

    transcript = []
    evidence = []

    transcript.append({"role": "user",
                       "content": "Process insurance claim %s. Start by calling "
                                  "get_claim with claim_id='%s'." % (case_id, case_id)})
    turns = 0
    iterations = 0
    tokens_in = tokens_out = 0
    stopped_by = None

    if approve is None:
        approve = lambda action, payload: True

    try:
        while True:
            iterations += 1
            if iterations > config.MAX_TURNS + 2:
                raise GuardrailStop("step_cap", "loop did not terminate")

            move = backend.next_move(transcript)
            ti, to = backend.token_estimate(transcript)
            tokens_in, tokens_out = tokens_in + ti, tokens_out + to
            guards.check_budget(tokens_in + tokens_out)

            if verbose:
                label = ("conclude" if "final" in move else "turn %d" % (turns + 1))
                print("  %-9s · %s" % (label, move.get("thought", "")[:88]))

            if "final" in move:
                record = dict(move["final"])
                break

            # ---- act: SEQUENTIAL — ONE call per turn ---------------
            turns += 1
            guards.check_turns(turns)

            calls = _normalize_calls(move)
            # SEQUENTIAL CHANGE: keep only the first call; the loop returns
            # for the next move to issue the remaining calls one at a time.
            calls = calls[:1]
            observations = []

            known = set(tools.REGISTRY.get(problem, {}))
            bad = [n for n, _ in calls if n not in known]
            if bad:
                record = {"decision": "escalate",
                          "reason": "model requested unknown tool(s): %s"
                                    % ", ".join(str(b) for b in bad)}
                break

            for name, args in calls:
                guards.check_duplicate(name, args)

                if name == tools.GATED_ACTION.get(problem):
                    if not guards.gate(name, args, approve):
                        raise GuardrailStop(
                            "gate_held",
                            "%s awaits human approval (autonomy=%s)"
                            % (name, config.AUTONOMY))

                result = tools.call(problem, name, args)
                evidence.append(name)
                observations.append({"tool": name, "args": args,
                                     "observation": result})
                if verbose:
                    print("       %-26s -> %s" % (name, _short(result)))

            transcript.append({"role": "assistant",
                               "content": move.get("thought", "")})
            transcript.append({"role": "user",
                               "content": repr(observations)})

    except GuardrailStop as stop:
        stopped_by = stop.reason
        record = {"decision": "escalate",
                  "reason": "halted by the %s guardrail - %s"
                            % (stop.reason, stop.detail)}

    cost = (tokens_in / 1e6) * config.PRICE_IN + (tokens_out / 1e6) * config.PRICE_OUT

    record.update({
        "case_id": case_id,
        "evidence": evidence,
        "turns": turns,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": round(cost, 6),
        "seconds": round(time.time() - started, 3),
        "guardrails_fired": guards.fired,
        "stopped_by": stopped_by,
        "backend": backend.name,
    })
    return record


def _short(value, n=64):
    s = repr(value)
    return s if len(s) <= n else s[:n - 1] + "…"
