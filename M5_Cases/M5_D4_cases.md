# M5 · D4 评估案例

本文件是我负责的评估案例的**权威规格**。每条都已在当前 git 仓库代码下用脚本化后端离线跑通、通过 code check。

## 案例清单

| 案例 ID | 场景 | 期望 decision | trigger | family |
|---|---|---|---|---|
| M5-CLM-9001 | act_multi | approve_in_principle | - | partly_payable |
| M5-CLM-9002 | ask_preauth_absent | request_document | - | preauth_absent |
| M5-CLM-9003 | escalate_duplicate | escalate | duplicate_claim | duplicate_of_decided_claim |
| M5-CLM-9004 | act_nonpanel | approve_in_principle | - | non_panel_hospital |
| M5-CLM-9005 | escalate_lapsed | escalate | policy_lapsed | policy_lapsed |
| M5-CLM-9006 | act_multi | approve_in_principle | - | mixed_disposition |

## 逐案例规格

### M5-CLM-9001

- 场景: `act_multi`
- 成员 / 医院 / 服务日期: M-2214 / H-114 / 2026-09-26
- 理赔项目: 47120=1400, 62480=780, 31255=300
- 期望 decision: `approve_in_principle`
- family: `partly_payable`
- 必须记录(must_record):
  - disposition per line
  - 31255 refused EX-14
  - PA-5521 cited 62480
  - approved_total 2180
  - refused_total 300
- 说明: 3 lines, each checked independently; 47120/62480 covered, 31255 refused EX-14.

### M5-CLM-9002

- 场景: `ask_preauth_absent`
- 成员 / 医院 / 服务日期: M-6118 / H-114 / 2026-09-27
- 理赔项目: 62480=2000
- 期望 decision: `request_document`
- 缺失文档(missing): pre-authorisation reference for line 62480, valid on 2026-09-27
- family: `preauth_absent`
- 必须记录(must_record):
  - the line (62480)
  - the date it must be valid on
- 说明: 62480 requires_preauth; coverage must be checked first, THEN preauth; no valid PA -> request.

### M5-CLM-9003

- 场景: `escalate_duplicate`
- 成员 / 医院 / 服务日期: M-2214 / H-114 / 2026-08-20
- 理赔项目: 47120=1500
- 期望 decision: `escalate`
- 期望 trigger: `duplicate_claim`
- family: `duplicate_of_decided_claim`
- 必须记录(must_record):
  - CLM-8710 named as prior decision
  - facts matched: member, hospital, date, lines
- 说明: Resubmission matching CLM-8710 on all four facts -> escalate.

### M5-CLM-9004

- 场景: `act_nonpanel`
- 成员 / 医院 / 服务日期: M-2214 / H-330 / 2026-09-28
- 理赔项目: 70553=2000
- 期望 decision: `approve_in_principle`
- family: `non_panel_hospital`
- 必须记录(must_record):
  - H-330 recorded as non-panel
  - approved_total 2000
  - record says member paid, claiming reimbursement
- 说明: H-330 non-panel: decision unchanged (approve), record reworded to member-paid reimbursement.

### M5-CLM-9005

- 场景: `escalate_lapsed`
- 成员 / 医院 / 服务日期: M-4471 / H-207 / 2026-04-18
- 理赔项目: 47120=1500
- 期望 decision: `escalate`
- 期望 trigger: `policy_lapsed`
- family: `policy_lapsed`
- 必须记录(must_record):
  - POL-5588 status lapsed
- 说明: Lapsed only surfaces after lookup_policy; escalate.

### M5-CLM-9006

- 场景: `act_multi`
- 成员 / 医院 / 服务日期: M-2214 / H-114 / 2026-09-29
- 理赔项目: 47120=1400, 31255=300, 62480=780
- 期望 decision: `approve_in_principle`
- family: `mixed_disposition`
- 必须记录(must_record):
  - 47120 covered
  - 31255 refused EX-14
  - 62480 covered, PA-5521 cited
  - per-line disposition
- 说明: 3 mixed lines: one covered, one excluded, one preauth valid. Three dispositions in one letter.
