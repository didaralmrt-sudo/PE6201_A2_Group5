# M4 · D7 两个复现的失败（Reproduced Failures）

D7 要求复现并解释**两个**失败。下面两个失败都在脚本化后端下由 `M4_guardrail_test.py` 的集成用例支撑，证明若缺失对应护栏，运行会失控。

## 失败 1 · 循环失控（runaway loop → step_cap）
**现象**：代理一直调用工具却不结案，turn 数无限增长。
**后果**：在 `MAX_TOKENS_PER_RUN` 预算内会先撞上 `budget_ceiling`；若预算也缺失，则无限 burning token。
**根因**：没有 step_cap 护栏，或护栏未真正中断循环。
**复现**：`M4_guardrail_test.py` 用例 **A1** 直接对 `Guardrails.check_turns` 做单元验证；集成上，用例 **B4** 用一个 20 步、**每次参数都不同**的脚本触发 `step_cap`（第 9 步，MAX_TURNS=8）。
**注意（实测）**：出厂配置下先"咬住"的其实是 `budget_ceiling`，不是 `step_cap`——`agent.py` 先查预算、后数回合，且 token 估算在第 9 次迭代就越过 60k。因此 B4 在**进程内临时抬高预算**（不改任何文件）以隔离步数上限；另见 `M4_D3b_guardrail_checklist.md` 的"必须写明的一句限制"。
**修复**：`guardrails.py` 的 `check_turns` 在 `turn > max_turns` 时抛出 `GuardrailStop("step_cap", ...)`，`agent.py` 捕获后记录 `stopped_by="step_cap"` 并以 escalate 结案。

## 失败 2 · 重复动作循环（duplicate-action loop → duplicate_action）
**现象**：代理对同一工具用相同参数反复调用，没有任何进展。
**后果**：Class 4 的历史失败——8 个 turn、无结论、成本 ~1.6x，且**没有抛异常**，只是空转烧钱。
**根因**：缺少动作去重护栏，循环没有"记忆"自己已经做过什么。
**复现**：`M4_guardrail_test.py` 用例 **B3**，脚本在同一 turn 内两次调用 `get_claim` 相同参数 → 触发 `duplicate_action`（敌意版本见用例 **H2\***）。
**修复**：`guardrails.py` 的 `check_duplicate` 用 `(tool, repr(sorted(args)))` 做签名去重，命中即抛出 `GuardrailStop("duplicate_action", ...)`，由 `agent.py` 转为 escalate 结案。

> 两个失败都通过"响亮地停止"（loud stop）来暴露问题：决策记录会写明 `stopped_by` 与触发的护栏，便于追溯，而不是静默返回一个空答案。
