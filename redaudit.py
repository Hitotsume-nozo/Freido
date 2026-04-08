import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Callable

from environment import FraudInvestigationEnv, TASKS
from models import Action, ActionType, SuspectRole


OUT_JSON = "./Exploit audit/red_team_audit_results.json"
OUT_MD = "./Exploit audit/RED_TEAM_REPORT.md"


@dataclass
class AttackResult:
    task_id: str
    attack: str
    ok: bool
    score: float
    steps: int
    done: bool
    last_error: Optional[str]
    notes: str = ""


def _step(env: FraudInvestigationEnv, action: Action):
    obs, reward, done, info = env.step(action)
    # reward.score can be delta or total depending on your env;
    # we treat it as the authoritative number returned.
    return obs, float(reward.score), done, info


def _reset(task_id: str) -> Tuple[FraudInvestigationEnv, Any]:
    env = FraudInvestigationEnv(task_id=task_id)
    obs = env.reset()
    return env, obs


def gold_evidence_ids(task_id: str) -> List[str]:
    gold = TASKS[task_id]["gold_labels"]
    return list(gold.get("key_evidence", {}).keys())


def gold_perpetrators(task_id: str) -> List[str]:
    gold = TASKS[task_id]["gold_labels"]
    return list(gold.get("perpetrators", {}).keys())


def non_perpetrators(task_id: str) -> List[str]:
    gold = TASKS[task_id]["gold_labels"]
    return list(gold.get("non_perpetrators", {}).keys())


def pick_innocent_for_attack(task_id: str) -> Optional[str]:
    gold = TASKS[task_id]["gold_labels"]
    nonp = gold.get("non_perpetrators", {}) or {}
    for name, info in nonp.items():
        if info.get("role") == "innocent":
            return name
    return next(iter(nonp.keys()), None)


def run_attack(
    task_id: str,
    attack_name: str,
    fn: Callable[[str], AttackResult],
) -> AttackResult:
    try:
        return fn(task_id)
    except Exception as e:
        return AttackResult(
            task_id=task_id,
            attack=attack_name,
            ok=False,
            score=0.0,
            steps=0,
            done=False,
            last_error=str(e),
            notes="Attack function raised exception (audit harness).",
        )


# -----------------------------
# Attacks
# -----------------------------


def attack_flag_without_examining(task_id: str) -> AttackResult:
    env, obs = _reset(task_id)
    target = gold_evidence_ids(task_id)[0]
    obs2, score, done, info = _step(
        env,
        Action(
            action_type=ActionType.FLAG_EVIDENCE,
            document_id=target,
            evidence_reason="Attempt to flag without examining first.",
        ),
    )
    steps = env.state().get("step_count", 0)
    # "ok" means exploit did NOT work (i.e., should error or not increase score meaningfully)
    ok = bool(obs2.last_action_error) or score <= 0.0001
    return AttackResult(
        task_id=task_id,
        attack="flag_without_examining",
        ok=ok,
        score=score,
        steps=steps,
        done=done,
        last_error=obs2.last_action_error,
        notes=f"Flagged doc_id={target} without examining. Expect error or ~0 reward.",
    )


def attack_accuse_without_evidence(task_id: str) -> AttackResult:
    env, obs = _reset(task_id)
    perp = gold_perpetrators(task_id)[0]
    obs2, score, done, info = _step(
        env,
        Action(
            action_type=ActionType.IDENTIFY_SUSPECT,
            person_name=perp,
            person_role=SuspectRole.MASTERMIND,
            evidence_ids=[],
            evidence_reason="Attempt to accuse without evidence_ids.",
        ),
    )
    steps = env.state().get("step_count", 0)
    ok = bool(obs2.last_action_error) or score <= 0.0001
    return AttackResult(
        task_id=task_id,
        attack="accuse_without_evidence",
        ok=ok,
        score=score,
        steps=steps,
        done=done,
        last_error=obs2.last_action_error,
        notes=f"Accused {perp} without evidence_ids. Expect error or ~0 reward.",
    )


def attack_duplicate_flagging(task_id: str) -> AttackResult:
    env, obs = _reset(task_id)
    target = gold_evidence_ids(task_id)[0]

    # examine
    obs, _, done, _ = _step(
        env, Action(action_type=ActionType.EXAMINE_DOCUMENT, document_id=target)
    )
    # flag once
    obs, score1, done, _ = _step(
        env,
        Action(
            action_type=ActionType.FLAG_EVIDENCE,
            document_id=target,
            evidence_reason="Flag #1",
        ),
    )
    # flag twice
    obs, score2, done, _ = _step(
        env,
        Action(
            action_type=ActionType.FLAG_EVIDENCE,
            document_id=target,
            evidence_reason="Flag #2",
        ),
    )

    steps = env.state().get("step_count", 0)

    # ok means second flag should not add benefit (score should not increase meaningfully)
    # depending on delta vs cumulative reward, we compare the second step reward directly.
    ok = (score2 <= score1) or (score2 <= 0.0001) or bool(obs.last_action_error)

    return AttackResult(
        task_id=task_id,
        attack="duplicate_flagging",
        ok=ok,
        score=score2,
        steps=steps,
        done=done,
        last_error=obs.last_action_error,
        notes=f"Flagged same doc twice: {target}. Second flag should not increase reward.",
    )


def attack_metadata_only_submit(task_id: str) -> AttackResult:
    env, obs = _reset(task_id)
    gold_scheme = TASKS[task_id]["gold_labels"]["scheme_type"]

    # Submit immediately without examining/flagging/accusing.
    obs, score, done, _ = _step(
        env,
        Action(
            action_type=ActionType.SUBMIT_REPORT,
            findings={"scheme_type": gold_scheme, "summary": "Metadata-only submit."},
        ),
    )
    steps = env.state().get("step_count", 0)

    # ok means metadata-only doesn't score high
    ok = score < 0.4
    return AttackResult(
        task_id=task_id,
        attack="metadata_only_submit",
        ok=ok,
        score=score,
        steps=steps,
        done=done,
        last_error=obs.last_action_error,
        notes="Immediate submit with correct scheme but no investigation.",
    )


def attack_evidence_spam(task_id: str) -> AttackResult:
    env, obs = _reset(task_id)
    # Examine first 6 docs (arbitrary) then flag all examined plus a few more.
    all_docs = [s.id for s in obs.available_sources]
    examine_ids = all_docs[:6]
    flag_ids = all_docs[:10]

    for doc_id in examine_ids:
        obs, _, done, _ = _step(
            env, Action(action_type=ActionType.EXAMINE_DOCUMENT, document_id=doc_id)
        )
        if done:
            break

    last_score = 0.0
    for doc_id in flag_ids:
        obs, last_score, done, _ = _step(
            env,
            Action(
                action_type=ActionType.FLAG_EVIDENCE,
                document_id=doc_id,
                evidence_reason="Spam flagging many docs.",
            ),
        )
        if done:
            break

    # Submit with correct scheme but no suspects/timeline
    scheme = TASKS[task_id]["gold_labels"]["scheme_type"]
    obs, last_score, done, _ = _step(
        env,
        Action(
            action_type=ActionType.SUBMIT_REPORT,
            findings={"scheme_type": scheme, "summary": "Spam evidence submit"},
        ),
    )

    steps = env.state().get("step_count", 0)

    # ok means spam doesn't get too high; threshold is heuristic.
    ok = last_score < 0.8
    return AttackResult(
        task_id=task_id,
        attack="evidence_spam",
        ok=ok,
        score=last_score,
        steps=steps,
        done=done,
        last_error=obs.last_action_error,
        notes="Examined a few docs, flagged many, submitted. Should be worse than precise case.",
    )


def attack_false_accusation(task_id: str) -> AttackResult:
    env, obs = _reset(task_id)
    gold_scheme = TASKS[task_id]["gold_labels"]["scheme_type"]
    gold_evs = gold_evidence_ids(task_id)[:4]

    # Examine + flag a few gold evidence docs (to set up a strong case)
    for doc_id in gold_evs:
        obs, _, done, _ = _step(
            env, Action(action_type=ActionType.EXAMINE_DOCUMENT, document_id=doc_id)
        )
        if done:
            break
    for doc_id in gold_evs:
        obs, _, done, _ = _step(
            env,
            Action(
                action_type=ActionType.FLAG_EVIDENCE,
                document_id=doc_id,
                evidence_reason="Gold evidence flag",
            ),
        )
        if done:
            break

    # Accuse a known innocent as mastermind
    target = pick_innocent_for_attack(task_id)
    if target:
        obs, score, done, _ = _step(
            env,
            Action(
                action_type=ActionType.IDENTIFY_SUSPECT,
                person_name=target,
                person_role=SuspectRole.MASTERMIND,
                evidence_ids=gold_evs[:2],
                evidence_reason="Intentionally false accusation.",
            ),
        )
    else:
        score = 0.0

    # Submit
    obs, score, done, _ = _step(
        env,
        Action(
            action_type=ActionType.SUBMIT_REPORT,
            findings={"scheme_type": gold_scheme, "summary": "False accusation submit"},
        ),
    )

    steps = env.state().get("step_count", 0)

    # ok means false accusation reduces score below near-perfect
    ok = score < 0.95
    return AttackResult(
        task_id=task_id,
        attack="false_accusation",
        ok=ok,
        score=score,
        steps=steps,
        done=done,
        last_error=obs.last_action_error,
        notes=f"Flagged some gold evidence, then falsely accused {target}. Score should drop noticeably.",
    )


# -----------------------------
# Reporting
# -----------------------------


def to_dict(r: AttackResult) -> Dict[str, Any]:
    return {
        "task_id": r.task_id,
        "attack": r.attack,
        "ok": r.ok,
        "score": round(float(r.score), 6),
        "steps": r.steps,
        "done": r.done,
        "last_error": r.last_error,
        "notes": r.notes,
    }


def markdown_report(all_results: List[AttackResult]) -> str:
    lines = []
    lines.append("# Red-Team Audit Report")
    lines.append("")
    lines.append(
        "This report runs adversarial probes against the environment to assess exploitability, fairness, and leakage."
    )
    lines.append("")
    lines.append("| Task | Attack | OK? | Score | Steps | Error | Notes |")
    lines.append("|---|---|---:|---:|---:|---|---|")

    for r in all_results:
        err = (r.last_error or "").replace("\n", " ")[:80]
        notes = (r.notes or "").replace("\n", " ")[:100]
        lines.append(
            f"| {r.task_id} | {r.attack} | {'OK' if r.ok else 'FAIL'} | {r.score:.4f} | {r.steps} | {err} | {notes} |"
        )

    lines.append("")
    lines.append("## How to interpret")
    lines.append("")
    lines.append(
        "- OK means the benchmark behaved as expected (attack did **not** succeed)."
    )
    lines.append(
        "- FAIL; means a potential hole: exploit worked, penalty too weak, or behavior was unintended."
    )
    lines.append("")
    lines.append("## Suggested follow-ups")
    lines.append("")
    lines.append(
        "- If `flag_without_examining` succeeds: require examination before flagging."
    )
    lines.append(
        "- If `accuse_without_evidence` succeeds: require evidence_ids and/or require evidence_ids be flagged."
    )
    lines.append(
        "- If `evidence_spam` scores high: increase irrelevant-evidence penalty or add precision term."
    )
    lines.append(
        "- If `false_accusation` remains near oracle: increase false accusation penalty and ensure it is not hidden by clamping."
    )
    lines.append("")
    return "\n".join(lines)


def main():
    task_ids = ["easy", "medium", "hard"]
    attack_fns = [
        ("flag_without_examining", attack_flag_without_examining),
        ("accuse_without_evidence", attack_accuse_without_evidence),
        ("duplicate_flagging", attack_duplicate_flagging),
        ("metadata_only_submit", attack_metadata_only_submit),
        ("evidence_spam", attack_evidence_spam),
        ("false_accusation", attack_false_accusation),
    ]

    results: List[AttackResult] = []
    for task_id in task_ids:
        for attack_name, fn in attack_fns:
            results.append(run_attack(task_id, attack_name, fn))

    # Write outputs
    json_out = {
        "results": [to_dict(r) for r in results],
        "summary": {
            "total": len(results),
            "ok": sum(1 for r in results if r.ok),
            "fail": sum(1 for r in results if not r.ok),
        },
    }

    Path(OUT_JSON).write_text(json.dumps(json_out, indent=2), encoding="utf-8")
    Path(OUT_MD).write_text(markdown_report(results), encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

    # Console summary
    fails = [r for r in results if not r.ok]
    if fails:
        print("\nFAILED / CONCERNING CASES:")
        for r in fails:
            print(
                f"- task={r.task_id} attack={r.attack} score={r.score:.4f} err={r.last_error}"
            )
    else:
        print("\nAll attacks behaved as expected.")


if __name__ == "__main__":
    main()
