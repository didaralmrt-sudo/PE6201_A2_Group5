"""
PE6201 · A2 scaffold — THE AGENT LOOP  (D1)
====================================================================
    thought -> action -> observation -> repeat -> final

That is the whole of ReAct, and it is hand-rolled here on purpose. No
framework owns your loop: when it misbehaves you need to be able to
read the twelve lines that did it.

WHAT MAKES THIS AN AGENT RATHER THAN A WORKFLOW: the number of steps is
decided by the DATA, not by you. A one-line claim with a live policy is
a short run. A four-line claim with a pre-authorisation to chase is a
long one. You did not write that branch - the record did.

--------------------------------------------------------------------
INSTRUMENTATION IS NOT OPTIONAL

Every run records turns, tokens, cost, every tool call and every
guardrail event. D6's cost model and D7's loop failure both need
numbers that were captured WHILE THE RUN HAPPENED. A team that adds
instrumentation afterwards has to run the whole battery again.

You cannot report a failure you had no way of noticing.
====================================================================
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
    whole --all run. A model that emits a malformed call simply gets no
    tool executed for that step, which is the safe failure.
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

    ISOLATION (D4): everything this function needs is created inside it.
    No case may depend on a previous one having run - so no module-level
    counters, no shared guardrail object, no leftover transcript.
    """
    problem = problem or config.PROBLEM
    started = time.time()

    guards = Guardrails(config.MAX_TURNS, config.MAX_TOKENS_PER_RUN,
                        config.AUTONOMY)
    # WHAT THE MODEL IS TOLD. On the scripted backend these are ignored -
    # the moves are pre-written, so no prompt is ever sent. On the live
    # backend this IS the experiment D2(b) measures: the descriptors and
    # the routing rules, assembled by prompt.build_system_prompt().
    #     python3 run_eval.py --prompt      to see the exact text
    backend = make_backend(
        case_id,
        tool_descriptors=[tools.DESCRIPTORS[n] for n in tools.REGISTRY[problem]
                          if n in tools.DESCRIPTORS],
        system_prompt=prompt.build_system_prompt(problem))

    transcript = []      # what the model would see
    evidence = []        # every tool actually called, in order

    transcript.append({"role": "user",
                       "content": "Process insurance claim %s. Start by calling "
                                  "get_claim with claim_id='%s'." % (case_id, case_id)})
    # TURNS ARE TOOL-CALLING TURNS. The concluding move - where the agent
    # writes its decision record - is bookkeeping, not a turn. This is the
    # same convention Appendix A uses: CLM-8842 is "turns": 4 with EIGHT
    # tool calls, because the gated action is a turn like any other and
    # the write-up afterwards is not. Count them any other way and your
    # D2(c) arithmetic stops agreeing with the brief.
    turns = 0
    iterations = 0       # loop-safety only; never reported
    tokens_in = tokens_out = 0
    stopped_by = None

    # On the scripted backend the gate auto-approves so the run stays
    # deterministic. The RECORD still shows the gate was reached and
    # passed, which is what a marker looks for.
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

            # A live model can return ANYTHING. From here down `move` is
            # treated as untrusted input: a shape we did not ask for must
            # end THIS run safely and never kill the whole --all battery.
            if not isinstance(move, dict):
                record = {"decision": "escalate",
                          "reason": "model returned a non-object move: %r" % (move,)}
                break

            if verbose:
                label = ("conclude" if "final" in move else "turn %d" % (turns + 1))
                print("  %-9s · %s" % (label, str(move.get("thought", ""))[:88]))

            # ---- conclude -------------------------------------------
            if "final" in move:
                final = move["final"]
                # Seen from llama-3.1-8b: {"final": null} and {"final": "text"}.
                # dict(None) raises "'NoneType' object is not iterable" and
                # killed the WHOLE --all run. Conclude safely instead.
                if isinstance(final, dict):
                    record = dict(final)
                else:
                    record = {"decision": "escalate",
                              "reason": "model returned a malformed final block: %r"
                                        % (final,)}
                break

            # ---- act: one turn may carry SEVERAL calls ---------------
            turns += 1
            guards.check_turns(turns)

            # Only calls INDEPENDENT of each other belong in one turn.
            # A dependency chain cannot be shortened by running things at
            # once - that is why Problem B saves less than Problem A.
            calls = _normalize_calls(move)
            observations = []

            # Defensive: a small model occasionally "calls" a tool that does
            # not exist (e.g. it emits {"tool":"escalate"} as if escalate were
            # an action). tools.call would raise KeyError and kill the WHOLE
            # --all run. Conclude safely instead.
            known = set(tools.REGISTRY.get(problem, {}))
            # A tiny model sometimes emits a tool NAME that is not even a
            # string (a nested list, a dict). `n not in known` on a set then
            # raises "unhashable type: 'list'" and kills the WHOLE --all run.
            # Treat any non-string or unknown name as a bad call and conclude
            # safely instead of crashing the battery.
            bad = [n for n, _ in calls if not isinstance(n, str) or n not in known]
            if bad:
                record = {"decision": "escalate",
                          "reason": "model requested unknown tool(s): %s"
                                    % ", ".join(str(b) for b in bad)}
                break

            for name, args in calls:
                guards.check_duplicate(name, args)

                # THE GATE goes in front of the irreversible step only.
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
        # A LOUD STOP. The record says what halted the run and where, so
        # this never looks like a quiet wrong answer.
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
