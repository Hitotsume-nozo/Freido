from environment import FraudInvestigationEnv
from models import Action, ActionType, SuspectRole, TimelineEvent


def step_ok(env, action):
    obs, reward, done, info = env.step(action)
    assert 0.0 <= reward.score <= 1.0
    return obs, reward, done, info


def examine_and_flag(env, doc_id: str, reason: str):
    obs, reward, done, info = step_ok(
        env,
        Action(action_type=ActionType.EXAMINE_DOCUMENT, document_id=doc_id),
    )
    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.FLAG_EVIDENCE,
            document_id=doc_id,
            evidence_reason=reason,
        ),
    )
    return obs, reward, done, info


def test_easy():
    print("\n=== Sanity test: easy ===")
    env = FraudInvestigationEnv("easy")
    obs = env.reset()

    # Strong gold evidence
    evidence = [
        ("exp_002", "Claimed dinner on March 12"),
        ("exp_003", "Claimed dinner on March 22"),
        ("ext_001", "Bella Italia was closed March 10-30"),
        ("email_004", "Sarah Lopez declined the March 12 dinner"),
        ("cal_001", "David was traveling during the claimed dinner period"),
        ("crm_002", "Lisa Park had not spoken to David in months"),
    ]

    for doc_id, reason in evidence:
        examine_and_flag(env, doc_id, reason)

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.IDENTIFY_SUSPECT,
            person_name="David Chen",
            person_role=SuspectRole.MASTERMIND,
            evidence_ids=[doc_id for doc_id, _ in evidence],
            evidence_reason="Submitted fake expense reports contradicted by closure, travel, and CRM records",
        ),
    )

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.ESTABLISH_TIMELINE,
            timeline_events=[
                TimelineEvent(
                    date="2024-03-11",
                    description="Sarah Lopez declined dinner invitation and was in San Francisco",
                    document_ids=["email_004"],
                ),
                TimelineEvent(
                    date="2024-03-12",
                    description="Expense report claimed a Bella Italia dinner while restaurant was closed and David was traveling",
                    document_ids=["exp_002", "ext_001", "cal_001"],
                ),
                TimelineEvent(
                    date="2024-04-03",
                    description="Expense report claimed dinner with Lisa Park despite no recent contact",
                    document_ids=["exp_004", "crm_002"],
                ),
            ],
        ),
    )

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.SUBMIT_REPORT,
            findings={
                "scheme_type": "expense_fraud",
                "summary": "David Chen fabricated client entertainment expenses using false dinner claims.",
            },
        ),
    )

    print("Easy breakdown:", reward.breakdown)
    print("Easy final:", reward.score)
    assert done is True
    assert reward.score >= 0.80


def test_medium():
    print("\n=== Sanity test: medium ===")
    env = FraudInvestigationEnv("medium")
    obs = env.reset()

    evidence = [
        ("vendor_001", "Apex vendor record names Carlos Martinez-Reeves"),
        ("ext_m01", "Corporate registry ties Apex to Carlos Martinez-Reeves"),
        ("fin_m01", "Sarah failed to disclose family business conflict"),
        ("proc_001", "Apex won at a large premium over lower bids"),
        ("proc_002", "Pattern repeated in second inflated contract"),
        ("proc_005", "Flagged contract still awarded to Apex"),
        ("email_m03", "James escalated concerns to CFO"),
        ("email_m05", "Sarah pressured James to stop objecting"),
        ("email_m07", "Sarah's personal email references coordination with 'C'"),
        (
            "market_001",
            "Apex prices are above market and vendor lacks industry presence",
        ),
    ]

    for doc_id, reason in evidence:
        examine_and_flag(env, doc_id, reason)

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.IDENTIFY_SUSPECT,
            person_name="Sarah Martinez",
            person_role=SuspectRole.MASTERMIND,
            evidence_ids=[
                "fin_m01",
                "email_m05",
                "email_m07",
                "proc_001",
                "proc_002",
                "proc_005",
            ],
            evidence_reason="Directed repeated overpriced awards to vendor tied to her husband and concealed the conflict.",
        ),
    )

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.IDENTIFY_SUSPECT,
            person_name="Carlos Martinez",
            person_role=SuspectRole.ACCOMPLICE,
            evidence_ids=["vendor_001", "ext_m01", "email_m07"],
            evidence_reason="Owned/controlled Apex Solutions and coordinated with Sarah.",
        ),
    )

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.ESTABLISH_TIMELINE,
            timeline_events=[
                TimelineEvent(
                    date="2023-02-10",
                    description="James Wilson raised concerns about Apex's first overpriced bid",
                    document_ids=["email_m01", "proc_001"],
                ),
                TimelineEvent(
                    date="2023-05-18",
                    description="James escalated repeated pricing concerns to the CFO",
                    document_ids=["email_m03", "proc_002"],
                ),
                TimelineEvent(
                    date="2023-08-08",
                    description="Sarah pressured James to stop objecting to Apex awards",
                    document_ids=["email_m05"],
                ),
                TimelineEvent(
                    date="2024-01-25",
                    description="Sarah's personal email revealed coordination with Carlos regarding the cybersecurity contract",
                    document_ids=["email_m07", "proc_005"],
                ),
            ],
        ),
    )

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.SUBMIT_REPORT,
            findings={
                "scheme_type": "vendor_kickback",
                "summary": "Sarah Martinez steered contracts to Apex Solutions, a vendor tied to her husband Carlos, at inflated prices.",
            },
        ),
    )

    print("Medium breakdown:", reward.breakdown)
    print("Medium final:", reward.score)
    assert done is True
    assert reward.score >= 0.75


def test_hard():
    print("\n=== Sanity test: hard ===")
    env = FraudInvestigationEnv("hard")
    obs = env.reset()

    evidence = [
        ("email_h01", "CFO initiated pressure to create contracts that 'look real'"),
        ("email_h05", "CFO directed aggressive revenue recognition"),
        ("email_h07", "CFO pressured Tom Baker to book the entries"),
        (
            "email_h02",
            "Lisa assigned fake account processing outside normal sales flow",
        ),
        ("email_h09", "Tom hid aging issues from standard reporting"),
        ("ext_h01", "NovaTech address is a UPS store"),
        ("ext_h02", "Quantum Dynamics is a virtual office"),
        ("ext_h03", "Pinnacle is effectively a shell / coworking hot desk"),
        (
            "ship_001",
            "No deployment activity or customer engagement for the fake accounts",
        ),
        ("fin_h03", "Bank records show zero payment from the fake customers"),
        ("crm_h01", "Fake deals skipped normal pipeline stages"),
        ("chat_h01", "Amy documented suspicions and fear"),
        ("inv_001", "CFO note shows awareness of investor reference-check risk"),
        ("board_001", "CFO presented inflated numbers to the board"),
    ]

    for doc_id, reason in evidence:
        examine_and_flag(env, doc_id, reason)

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.IDENTIFY_SUSPECT,
            person_name="Robert Kim",
            person_role=SuspectRole.MASTERMIND,
            evidence_ids=[
                "email_h01",
                "email_h05",
                "email_h07",
                "inv_001",
                "board_001",
            ],
            evidence_reason="Initiated the fraud, directed improper recognition, pressured finance, and used false metrics for fundraising.",
        ),
    )

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.IDENTIFY_SUSPECT,
            person_name="Lisa Wang",
            person_role=SuspectRole.ACCOMPLICE,
            evidence_ids=["email_h02", "crm_h01", "ext_h01", "ext_h02", "ext_h03"],
            evidence_reason="Created or routed fake deals into the pipeline and bypassed normal sales qualification.",
        ),
    )

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.IDENTIFY_SUSPECT,
            person_name="Tom Baker",
            person_role=SuspectRole.RELUCTANT_PARTICIPANT,
            evidence_ids=["email_h05", "email_h07", "email_h09"],
            evidence_reason="Under pressure from the CFO, booked and concealed fraudulent revenue despite recognizing the issues.",
        ),
    )

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.ESTABLISH_TIMELINE,
            timeline_events=[
                TimelineEvent(
                    date="2023-07-10",
                    description="Robert Kim pushed for fabricated-looking enterprise growth ahead of Series C",
                    document_ids=["email_h01"],
                ),
                TimelineEvent(
                    date="2023-08-20",
                    description="Lisa routed fake customer paperwork through Amy outside normal sales process",
                    document_ids=["email_h02", "chat_h01"],
                ),
                TimelineEvent(
                    date="2023-10-20",
                    description="Robert directed Tom to recognize unsupported revenue for fake customers",
                    document_ids=["email_h05", "email_h07"],
                ),
                TimelineEvent(
                    date="2023-11-05",
                    description="Inflated numbers were presented to the board as genuine growth",
                    document_ids=["board_001"],
                ),
                TimelineEvent(
                    date="2024-01-20",
                    description="Investor deck still used fake customer metrics while CFO worried about reference checks",
                    document_ids=["inv_001", "fin_h03"],
                ),
            ],
        ),
    )

    obs, reward, done, info = step_ok(
        env,
        Action(
            action_type=ActionType.SUBMIT_REPORT,
            findings={
                "scheme_type": "revenue_fabrication",
                "summary": "Robert Kim orchestrated a revenue fabrication scheme using shell customers, Lisa Wang operationalized fake deals, and Tom Baker booked and concealed the numbers under pressure.",
            },
        ),
    )

    print("Hard breakdown:", reward.breakdown)
    print("Hard final:", reward.score)
    assert done is True
    assert reward.score >= 0.75


def main():
    test_easy()
    test_medium()
    test_hard()
    print("\nAll sanity tests passed.")


if __name__ == "__main__":
    main()
