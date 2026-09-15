"""
M1 · D2(c) reproducible runner — runs the SAME evaluation set through
BOTH the parallel agent (`agent.py`) and the sequential agent
(`agent_sequential.py`) on the free scripted backend, and prints the
turns / tokens / cost / code-check for each.

    python run_d2c.py

This is the code-level proof behind `M1_D2c_sequential_vs_parallel.md`.
Turns and pass-rate are exact; token/cost columns are SCRIPTED ESTIMATES
(the scripted backend does not call an LLM, so usage is estimated).

Note: on the scripted backend, "parallel vs sequential" is decided by how
the script groups calls. This runner therefore runs `agent.py` against the
packed script and `agent_sequential.py` against the one-call-per-turn
(split) script — the sequential agent executes exactly one call per turn.
"""
import config
import backends
import harness
import agent
import agent_sequential

# D2(c) compares scheduling on the free scripted backend (no LLM cost).
# Force it here so the runner is self-contained regardless of config.py.
config.PROBLEM = "A"
config.BACKEND = "scripted"

# Lift safety caps so neither mode is halted mid-run by a guardrail
# (see the note in M1_D2c_sequential_vs_parallel.md: on the shipped cap the
# sequential CLM-8842 / CLM-8960 trip the budget ceiling — itself evidence).
config.MAX_TOKENS_PER_RUN = 5_000_000
config.MAX_TURNS = 40

KEY = harness.load_key("A")

# M1's D2(c) evaluation set: the teacher's CLM-8842 (already in
# backends.SCRIPTS) PLUS M1's 6 newly authored cases = 7 cases.
# Restricted to this set so the output matches M1_D2c_sequential_vs_parallel.md
# exactly (the scaffold also ships REF-* reference cases that are NOT M1's).
M1_CASE_IDS = ["CLM-8842", "CLM-8850", "CLM-8960", "CLM-8861",
               "CLM-8910", "CLM-8888", "CLM-8933"]


def to_sequential(script):
    seq = []
    for step in script:
        if "final" in step:
            seq.append(step)
            continue
        for name, args in step["calls"]:
            seq.append({"thought": step.get("thought", "") + " [seq]",
                        "calls": [(name, args)]})
    return seq


def run_variant(case_id, script, module):
    saved = backends.SCRIPTS.get(case_id)
    backends.SCRIPTS[case_id] = script
    try:
        rec = module.run_case(case_id, problem="A")
        exp = KEY.get(case_id, {})
        passed, fails = harness.code_check(rec, exp)
        return rec, passed
    finally:
        if saved is None:
            backends.SCRIPTS.pop(case_id, None)
        else:
            backends.SCRIPTS[case_id] = saved


print("=" * 78)
print("M1 · D2(c)  PARALLEL (agent.py) vs SEQUENTIAL (agent_sequential.py)")
print("=" * 78)
print("case         mode        turns  tok_in  tok_out  cost($)   code_check")
print("-" * 78)

tp_t = ts_t = tp_k = ts_k = 0
tp_c = ts_c = 0
n_pass = 0
for cid in M1_CASE_IDS:
    if cid not in backends.SCRIPTS:
        print("%-12s (script not found in backends.SCRIPTS - skipped)" % cid)
        continue
    pscript = backends.SCRIPTS[cid]
    rp, pp = run_variant(cid, pscript, agent)
    rs, ps = run_variant(cid, to_sequential(pscript), agent_sequential)
    if pp and ps:
        n_pass += 1
    tp_t += rp["turns"]; ts_t += rs["turns"]
    tp_k += rp["tokens_in"]; ts_k += rs["tokens_in"]
    tp_c += rp["cost_usd"]; ts_c += rs["cost_usd"]
    print("%-12s %-10s %5d  %6d  %6d  %8.5f   %s"
          % (cid, "parallel", rp["turns"], rp["tokens_in"], rp["tokens_out"],
             rp["cost_usd"], "PASS" if pp else "FAIL"))
    print("%-12s %-10s %5d  %6d  %6d  %8.5f   %s"
          % (cid, "sequential", rs["turns"], rs["tokens_in"], rs["tokens_out"],
             rs["cost_usd"], "PASS" if ps else "FAIL"))

print("-" * 78)
print("TOTALS  parallel:   %d turns, %d tok_in, $%.5f" % (tp_t, tp_k, tp_c))
print("        sequential: %d turns, %d tok_in, $%.5f" % (ts_t, ts_k, ts_c))
print("        turn reduction: %.0f%%" % (100 * (1 - tp_t / ts_t)))
print("        pass rate: %d/%d cases pass in BOTH modes (unchanged)."
      % (n_pass, len(M1_CASE_IDS)))
print("=" * 78)
print("tokens/cost are SCRIPTED ESTIMATES; turns and pass-rate are exact.")
