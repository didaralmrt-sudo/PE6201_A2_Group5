# M5 - D4 Evaluation Cases

Here are the final specs for my assigned evaluation cases. I've already tested all of them offline using the scripted backend on the current repo branch, and they all pass the code checks.

## Case Summary
| Case ID | Scenario | Expected Decision | Trigger | Family |
| :--- | :--- | :--- | :--- | :--- |
| M5-CLM-9001 | act_multi | approve_in_principle | - | partly_payable |
| M5-CLM-9002 | ask_preauth_absent | request_document | - | preauth_absent |
| M5-CLM-9003 | escalate_duplicate | escalate | duplicate_claim | duplicate_of_decided_claim |
| M5-CLM-9004 | act_nonpanel | approve_in_principle | - | non_panel_hospital |
| M5-CLM-9005 | escalate_lapsed | escalate | policy_lapsed | policy_lapsed |
| M5-CLM-9006 | act_multi | approve_in_principle | - | mixed_disposition |
**

## Detailed Case Specs

### M5-CLM-9001
- **Scenario:** act_multi
- **Member / Hospital / DOS:** M-2214 / H-114 / 2026-09-26
- **Claimed Items:** 47120=1400, 62480=780, 31255=300
- **Expected Decision:** approve_in_principle
- **Family:** partly_payable
- **Must Record:**
  - disposition per line
  - 31255 refused EX-14
  - PA-5521 cited 62480
  - approved_total 2180
  - refused_total 300
- **Notes:** We have 3 lines here, and we check each one independently. 47120 and 62480 are covered, but 31255 gets rejected due to EX-14.

### M5-CLM-9002
- **Scenario:** ask_preauth_absent
- **Member / Hospital / DOS:** M-6118 / H-114 / 2026-09-27
- **Claimed Items:** 62480=2000
- **Expected Decision:** request_document
- **Missing:** pre-authorisation reference for line 62480, valid on 2026-09-27
- **Family:** preauth_absent
- **Must Record:**
  - the line (62480)
  - the date it must be valid on
- **Notes:** Procedure 62480 requires a pre-auth. The system needs to check coverage first, then pre-auth. Since there's no valid PA, it should output a document request.

### M5-CLM-9003
- **Scenario:** escalate_duplicate
- **Member / Hospital / DOS:** M-2214 / H-114 / 2026-08-20
- **Claimed Items:** 47120=1500
- **Expected Decision:** escalate
- **Trigger:** duplicate_claim
- **Family:** duplicate_of_decided_claim
- **Must Record:**
  - CLM-8710 named as prior decision
  - facts matched: member, hospital, date, lines
- **Notes:** This is a resubmission. It matches CLM-8710 on all four facts (member, hospital, date, lines), so it should just escalate.

### M5-CLM-9004
- **Scenario:** act_nonpanel
- **Member / Hospital / DOS:** M-2214 / H-330 / 2026-09-28
- **Claimed Items:** 70553=2000
- **Expected Decision:** approve_in_principle
- **Family:** non_panel_hospital
- **Must Record:**
  - H-330 recorded as non-panel
  - approved_total 2000
  - record says member paid, claiming reimbursement
- **Notes:** Since H-330 is a non-panel hospital, the overall decision stays as an approval, but the record needs to reflect that the member paid upfront and is claiming reimbursement.

### M5-CLM-9005
- **Scenario:** escalate_lapsed
- **Member / Hospital / DOS:** M-4471 / H-207 / 2026-04-18
- **Claimed Items:** 47120=1500
- **Expected Decision:** escalate
- **Trigger:** policy_lapsed
- **Family:** policy_lapsed
- **Must Record:**
  - POL-5588 status lapsed
- **Notes:** The lapsed status only surfaces after hitting the lookup_policy tool. Once seen, the system needs to escalate immediately.

### M5-CLM-9006
- **Scenario:** act_multi
- **Member / Hospital / DOS:** M-2214 / H-114 / 2026-09-29
- **Claimed Items:** 47120=1400, 31255=300, 62480=780
- **Expected Decision:** approve_in_principle
- **Family:** mixed_disposition
- **Must Record:**
  - 47120 covered
  - 31255 refused EX-14
  - 62480 covered, PA-5521 cited
  - per-line disposition
- **Notes:** Dealing with 3 mixed lines here: one covered, one excluded, and one with a valid pre-auth. The final letter needs to combine all three dispositions into one.
