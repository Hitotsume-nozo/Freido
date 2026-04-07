# smoke_test.py
from environment import FraudInvestigationEnv
from models import Action, ActionType, SuspectRole


def test_task(task_id: str):
    print(f"\n=== Testing task: {task_id} ===")
    env = FraudInvestigationEnv(task_id=task_id)

    obs = env.reset()
    assert obs.task_id == task_id
    assert obs.step_number == 0
    assert obs.max_steps > 0
    assert len(obs.available_sources) > 0
    print(f"Reset OK: {len(obs.available_sources)} sources")

    # Examine first doc
    first_doc = obs.available_sources[0].id
    obs, reward, done, info = env.step(
        Action(action_type=ActionType.EXAMINE_DOCUMENT, document_id=first_doc)
    )
    assert obs.step_number == 1
    assert obs.document_content is not None
    assert 0.0 <= reward.score <= 1.0
    assert done is False
    print("Examine OK")

    # Search
    obs, reward, done, info = env.step(
        Action(action_type=ActionType.SEARCH_RECORDS, query="David")
    )
    assert 0.0 <= reward.score <= 1.0
    print("Search OK")

    # Flag evidence
    target_doc = obs.available_sources[0].id
    obs, reward, done, info = env.step(
        Action(
            action_type=ActionType.FLAG_EVIDENCE,
            document_id=target_doc,
            evidence_reason="Testing evidence flagging",
        )
    )
    assert len(obs.flagged_evidence) >= 1
    assert 0.0 <= reward.score <= 1.0
    print("Flag evidence OK")

    # Identify suspect
    obs, reward, done, info = env.step(
        Action(
            action_type=ActionType.IDENTIFY_SUSPECT,
            person_name="Test Suspect",
            person_role=SuspectRole.WITNESS,
            evidence_reason="Testing suspect identification",
        )
    )
    assert len(obs.identified_suspects) >= 1
    assert 0.0 <= reward.score <= 1.0
    print("Identify suspect OK")

    # Submit
    obs, reward, done, info = env.step(
        Action(
            action_type=ActionType.SUBMIT_REPORT,
            findings={"scheme_type": "expense_fraud", "summary": "Test submission"},
        )
    )
    assert done is True
    assert 0.0 <= reward.score <= 1.0
    print("Submit OK")
    print(f"Final reward: {reward.score:.4f}")


def main():
    for task_id in ["easy", "medium", "hard"]:
        test_task(task_id)
    print("\nAll smoke tests passed.")


if __name__ == "__main__":
    main()
