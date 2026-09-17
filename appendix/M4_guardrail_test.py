#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M4 护栏行为自检：直接调用仓库的 guardrails.py / agent.py。
运行：python M4_guardrail_test.py [<仓库A2_scaffold目录或仓库根目录>]
期望：7/7 PASS。
"""
import os, sys, importlib.util

def find_scaffold():
    if len(sys.argv) > 1:
        a = sys.argv[1]
        if os.path.isfile(os.path.join(a, "backends.py")):
            return a
        if os.path.isfile(os.path.join(a, "A2_scaffold", "backends.py")):
            return os.path.join(a, "A2_scaffold")
    here = os.path.dirname(os.path.abspath(__file__))
    bases = [here]
    b = here
    for _ in range(5):
        b = os.path.dirname(b)
        bases.append(b)
    for base in bases:
        for _ in range(3):
            p = os.path.join(base, "A2_scaffold")
            if os.path.isfile(os.path.join(p, "backends.py")):
                return p
            p2 = os.path.join(base, "PE6201_A2_GROUP5", "A2_scaffold")
            if os.path.isfile(os.path.join(p2, "backends.py")):
                return p2
            base = os.path.dirname(base)
    cands = [r"D:\NTU learning\Tri1\PE6201\PE6201_A2_GROUP5\A2_scaffold"]
    for c in cands:
        if os.path.isfile(os.path.join(c, "backends.py")):
            return c
    return None

SCAF = find_scaffold()
if not SCAF:
    sys.exit("找不到 A2_scaffold/backends.py，请在参数里给出仓库路径。")
sys.path.insert(0, SCAF)
import config, guardrails as gr, backends, agent

def run_with(script, case_id="TEST-X"):
    backends.SCRIPTS[case_id] = script
    return agent.run_case(case_id)

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("  PASS " if cond else "  FAIL ") + name + (("  -- " + detail) if detail and not cond else ""))

# 1) step_cap
g = gr.Guardrails(8, 60000, "confirm")
try:
    for t in range(1, 30):
        g.check_turns(t)
    check("step_cap fires", False, "did not fire")
except gr.GuardrailStop as e:
    check("step_cap fires", e.reason == "step_cap", e.reason)

# 2) budget_ceiling
g = gr.Guardrails(8, 2000, "confirm")
try:
    g.check_budget(3000)
    check("budget_ceiling fires", False, "did not fire")
except gr.GuardrailStop as e:
    check("budget_ceiling fires", e.reason == "budget_ceiling", e.reason)

# 3) duplicate_action (de-dup)
g = gr.Guardrails(8, 60000, "confirm")
try:
    g.check_duplicate("get_claim", {"claim_id": "X"})
    g.check_duplicate("get_claim", {"claim_id": "X"})
    check("duplicate_action fires", False, "did not fire")
except gr.GuardrailStop as e:
    check("duplicate_action fires", e.reason == "duplicate_action", e.reason)

# 4) gate_passed (confirm + approve True)
g = gr.Guardrails(8, 60000, "confirm")
ok = g.gate("issue_decision_letter", {}, lambda a, p: True)
check("gate_passed on confirm+approve",
      ok is True and any(f["guardrail"] == "gate_passed" for f in g.fired), str(g.fired))

# 5) gate_held (confirm + approve False)
g = gr.Guardrails(8, 60000, "confirm")
ok = g.gate("issue_decision_letter", {}, lambda a, p: False)
check("gate_held on confirm+deny",
      ok is False and any(f["guardrail"] == "gate_held" for f in g.fired), str(g.fired))

# 6) loop integration: duplicate action stops the run
dup = {"TEST-DUP": [{"calls": [("get_claim", {"claim_id": "X"}),
                                ("get_claim", {"claim_id": "X"})]}]}
res = run_with(dup["TEST-DUP"], "TEST-DUP")
fired = [f["guardrail"] for f in res["guardrails_fired"]]
check("loop duplicate_action (integration)", "duplicate_action" in fired, str(fired))

# 7) unknown tool -> safe escalate, no crash
unk = {"TEST-UNK": [{"calls": [("escalate_now", {})]}]}
res = run_with(unk["TEST-UNK"], "TEST-UNK")
check("unknown tool -> escalate", res.get("decision") == "escalate", str(res.get("decision")))

passed = sum(1 for _, c in results if c)
print("\nGuardrail test: %d/%d passed" % (passed, len(results)))
sys.exit(0 if passed == len(results) else 1)
