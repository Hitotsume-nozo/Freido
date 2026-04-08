import json
import random
import statistics
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

from environment import FraudInvestigationEnv, TASKS
from models import Action, ActionType, SuspectRole, TimelineEvent

try:
    # Optional: reuse your submitted fallback report logic if available
    from inference import task_aware_fallback_report
except Exception:
    task_aware_fallback_report = None


OUTPUT_JSON = "./Benchmark_audit/benchmark_audit_results.json"
OUTPUT_MD = "./Benchmark_audit/BENCHMARK_AUDIT.md"

SCHEME_VALUES = [
    "expense_fraud",
    "vendor_kickback",
    "revenue_fabrication",
    "embezzlement",
    "money_laundering",
    "payroll_fraud",
]

ROLE_MAP = {
    "mastermind": SuspectRole.MASTERMIND,
    "accomplice": SuspectRole.ACCOMPLICE,
    "reluctant_participant": SuspectRole.RELUCTANT_PARTICIPANT,
    "witness": SuspectRole.WITNESS,
    "innocent": SuspectRole.INNOCENT,
}


def role_from_string(name: str) -> SuspectRole:
    return ROLE_MAP[name]


def get_task(task_id: str) -> Dict[str, Any]:
    return TASKS[task_id]


def get_docs(task_id: str) -> Dict[str, Dict[str, Any]]:
    return get_task(task_id)["documents"]


def get_gold(task_id: str) -> Dict[str, Any]:
    return get_task(task_id)["gold_labels"]


def extract_all_known_people(task_id: str) -> List[str]:
    gold = get_gold(task_id)
    names = set()

    for name in gold.get("perpetrators", {}).keys():
        names.add(name)
        for alias in gold["perpetrators"][name].get("aliases", []):
            names.add(alias)

    for name in gold.get("non_perpetrators", {}).keys():
        names.add(name)

    # Also parse employee record titles as a fallback
    for doc in get_docs(task_id).values():
        title = doc.get("title", "")
        if title.startswith("Employee Record - "):
            names.add(title.replace("Employee Record - ", "").strip())

    return sorted(names)


def pick_false_accusation_target(task_id: str) -> Optional[str]:
    gold = get_gold(task_id)
    non_perps = gold.get("non_perpetrators", {})

    # Prefer clearly innocent people first
    for name, info in non_perps.items():
        if info.get("role") == "innocent":
            return name

    # Then any non-perp
    for name in non_perps.keys():
        return name

    # Fallback: any non-perp parsed from docs
    perps = set(gold.get("perpetrators", {}).keys())
    for person in extract_all_known_people(task_id):
        if person not in perps:
            return person

    return None


def irrelevant_doc_ids(task_id: str, limit: int = 4) -> List[str]:
    docs = get_docs(task_id)
    gold = get_gold(task_id)
    gold_evidence = set(gold.get("key_evidence", {}).keys())

    out = []
    for doc_id in docs.keys():
        if doc_id not in gold_evidence:
            out.append(doc_id)
        if len(out) >= limit:
            break
    return out


def sort_doc_ids_by_date(task_id: str, doc_ids: List[str]) -> List[str]:
    docs = get_docs(task_id)

    def key_fn(doc_id: str):
        return docs[doc_id].get("date") or "9999-99-99"

    return sorted(doc_ids, key=key_fn)


def build_timeline_from_doc_ids(
    task_id: str,
    doc_ids: List[str],
    limit: int = 3,
) -> List[TimelineEvent]:
    docs = get_docs(task_id)
    gold = get_gold(task_id)
    key_reasons = {
        doc_id: meta["reason"] for doc_id, meta in gold.get("key_evidence", {}).items()
    }

    timeline = []
    for doc_id in sort_doc_ids_by_date(task_id, doc_ids)[:limit]:
        doc = docs[doc_id]
        date = doc.get("date") or "unknown"
        description = key_reasons.get(
            doc_id, doc.get("title", f"Evidence from {doc_id}")
        )
        timeline.append(
            TimelineEvent(
                date=date,
                description=description,
                document_ids=[doc_id],
            )
        )
    return timeline


def ensure_unique_evidence_items(
    evidence: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    seen = set()
    out = []
    for item in evidence:
        doc_id = item["document_id"]
        if doc_id in seen:
            continue
        seen.add(doc_id)
        out.append(item)
    return out


def build_oracle_report(task_id: str) -> Dict[str, Any]:
    gold = get_gold(task_id)

    evidence_items = []
    for doc_id, meta in gold.get("key_evidence", {}).items():
        evidence_items.append(
            {
                "document_id": doc_id,
                "reason": meta["reason"],
            }
        )

    suspects = []
    for name, info in gold.get("perpetrators", {}).items():
        suspects.append(
            {
                "name": name,
                "role": info["role"],
                "evidence_ids": list(gold.get("key_evidence", {}).keys())[:6],
                "reasoning": f"{name} is a supported perpetrator in the gold investigation record.",
            }
        )

    timeline_limit = {
        "easy": 3,
        "medium": 4,
        "hard": 5,
    }[task_id]

    timeline = build_timeline_from_doc_ids(
        task_id,
        list(gold.get("key_evidence", {}).keys()),
        limit=timeline_limit,
    )

    return {
        "scheme_type": gold["scheme_type"],
        "summary": f"Oracle reconstruction for {gold['scheme_type']}.",
        "evidence": ensure_unique_evidence_items(evidence_items),
        "suspects": suspects,
        "timeline": [
            {
                "date": t.date,
                "description": t.description,
                "document_ids": t.document_ids,
            }
            for t in timeline
        ],
    }


def build_false_accusation_report(task_id: str) -> Dict[str, Any]:
    report = build_oracle_report(task_id)
    target = pick_false_accusation_target(task_id)

    if target is not None:
        report["suspects"].append(
            {
                "name": target,
                "role": "mastermind",
                "evidence_ids": [e["document_id"] for e in report["evidence"][:2]],
                "reasoning": f"Intentionally over-aggressive accusation against {target}.",
            }
        )

    return report


def build_overinclusive_report(task_id: str) -> Dict[str, Any]:
    report = build_oracle_report(task_id)

    for doc_id in irrelevant_doc_ids(task_id, limit=4):
        report["evidence"].append(
            {
                "document_id": doc_id,
                "reason": f"Overinclusive evidence inclusion for {doc_id}.",
            }
        )

    target = pick_false_accusation_target(task_id)
    if target is not None:
        report["suspects"].append(
            {
                "name": target,
                "role": "accomplice",
                "evidence_ids": [e["document_id"] for e in report["evidence"][:2]],
                "reasoning": f"Overinclusive case incorrectly implicates {target}.",
            }
        )

    report["evidence"] = ensure_unique_evidence_items(report["evidence"])
    return report


def build_read_only_doc_set(task_id: str) -> List[str]:
    return list(get_gold(task_id).get("key_evidence", {}).keys())


def execute_report_policy(task_id: str, report: Dict[str, Any]) -> Dict[str, Any]:
    env = FraudInvestigationEnv(task_id=task_id)
    obs = env.reset()

    examined = set()

    # Examine all docs needed by evidence / suspects / timeline before acting
    required_doc_ids = []
    for item in report.get("evidence", []):
        required_doc_ids.append(item["document_id"])

    for suspect in report.get("suspects", []):
        required_doc_ids.extend(suspect.get("evidence_ids", []))

    for event in report.get("timeline", []):
        required_doc_ids.extend(event.get("document_ids", []))

    required_doc_ids = sort_doc_ids_by_date(
        task_id, list(dict.fromkeys(required_doc_ids))
    )

    final_reward = None
    done = False

    for doc_id in required_doc_ids:
        if done:
            break
        if doc_id in examined:
            continue
        obs, reward, done, info = env.step(
            Action(action_type=ActionType.EXAMINE_DOCUMENT, document_id=doc_id)
        )
        final_reward = reward
        examined.add(doc_id)

    # Flag evidence
    for item in report.get("evidence", []):
        if done:
            break
        obs, reward, done, info = env.step(
            Action(
                action_type=ActionType.FLAG_EVIDENCE,
                document_id=item["document_id"],
                evidence_reason=item["reason"],
            )
        )
        final_reward = reward

    # Identify suspects
    for suspect in report.get("suspects", []):
        if done:
            break
        role = role_from_string(suspect["role"])
        obs, reward, done, info = env.step(
            Action(
                action_type=ActionType.IDENTIFY_SUSPECT,
                person_name=suspect["name"],
                person_role=role,
                evidence_ids=suspect.get("evidence_ids", []),
                evidence_reason=suspect.get("reasoning", ""),
            )
        )
        final_reward = reward

    # Timeline
    if not done and report.get("timeline"):
        timeline_events = []
        for event in report["timeline"]:
            timeline_events.append(
                TimelineEvent(
                    date=event["date"],
                    description=event["description"],
                    document_ids=event["document_ids"],
                )
            )

        obs, reward, done, info = env.step(
            Action(
                action_type=ActionType.ESTABLISH_TIMELINE,
                timeline_events=timeline_events,
            )
        )
        final_reward = reward

    # Submit
    if not done:
        obs, reward, done, info = env.step(
            Action(
                action_type=ActionType.SUBMIT_REPORT,
                findings={
                    "scheme_type": report["scheme_type"],
                    "summary": report.get("summary", ""),
                },
            )
        )
        final_reward = reward

    final_state = env.state()

    return {
        "score": final_reward.score if final_reward else 0.0,
        "breakdown": final_reward.breakdown if final_reward else {},
        "steps": final_state.get("step_count", 0),
        "done": done,
    }


def run_scheme_only_submit(task_id: str) -> Dict[str, Any]:
    env = FraudInvestigationEnv(task_id=task_id)
    env.reset()
    scheme = get_gold(task_id)["scheme_type"]
    obs, reward, done, info = env.step(
        Action(
            action_type=ActionType.SUBMIT_REPORT,
            findings={
                "scheme_type": scheme,
                "summary": "Immediate submit using only scheme prior.",
            },
        )
    )
    return {
        "score": reward.score,
        "breakdown": reward.breakdown,
        "steps": env.state().get("step_count", 0),
        "done": done,
    }


def run_read_only_then_submit(task_id: str) -> Dict[str, Any]:
    env = FraudInvestigationEnv(task_id=task_id)
    env.reset()

    final_reward = None
    done = False
    for doc_id in build_read_only_doc_set(task_id):
        if done:
            break
        obs, reward, done, info = env.step(
            Action(action_type=ActionType.EXAMINE_DOCUMENT, document_id=doc_id)
        )
        final_reward = reward

    if not done:
        scheme = get_gold(task_id)["scheme_type"]
        obs, reward, done, info = env.step(
            Action(
                action_type=ActionType.SUBMIT_REPORT,
                findings={
                    "scheme_type": scheme,
                    "summary": "Read documents but did not structure findings.",
                },
            )
        )
        final_reward = reward

    return {
        "score": final_reward.score if final_reward else 0.0,
        "breakdown": final_reward.breakdown if final_reward else {},
        "steps": env.state().get("step_count", 0),
        "done": done,
    }


def run_fallback_baseline(task_id: str) -> Optional[Dict[str, Any]]:
    if task_aware_fallback_report is None:
        return None

    task = get_task(task_id)
    allowed_doc_ids = list(task["documents"].keys())
    report = task_aware_fallback_report(task_id, allowed_doc_ids)
    return execute_report_policy(task_id, report)


def run_oracle_case(task_id: str) -> Dict[str, Any]:
    report = build_oracle_report(task_id)
    return execute_report_policy(task_id, report)


def run_false_accusation_case(task_id: str) -> Dict[str, Any]:
    report = build_false_accusation_report(task_id)
    return execute_report_policy(task_id, report)


def run_overinclusive_case(task_id: str) -> Dict[str, Any]:
    report = build_overinclusive_report(task_id)
    return execute_report_policy(task_id, report)


def run_random_policy_once(task_id: str, seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    env = FraudInvestigationEnv(task_id=task_id)
    env.reset()

    docs = list(get_docs(task_id).keys())
    known_people = extract_all_known_people(task_id)
    examined = []
    flagged = []

    max_steps = get_task(task_id)["max_steps"]
    final_reward = None
    done = False

    # Reserve 1 final step for submit
    for _ in range(max_steps - 1):
        if done:
            break

        possible_actions = []

        # Examine random unseen doc
        unseen = [d for d in docs if d not in examined]
        if unseen:
            possible_actions.append("examine")

        # Flag random examined doc
        if examined:
            possible_actions.append("flag")

        # Identify random suspect
        if flagged and known_people:
            possible_actions.append("suspect")

        # Sometimes search/cross-ref not used here to keep policy simple and legal
        if not possible_actions:
            break

        choice = rng.choice(possible_actions)

        if choice == "examine":
            doc_id = rng.choice(unseen)
            obs, reward, done, info = env.step(
                Action(action_type=ActionType.EXAMINE_DOCUMENT, document_id=doc_id)
            )
            examined.append(doc_id)
            final_reward = reward

        elif choice == "flag":
            doc_id = rng.choice(examined)
            obs, reward, done, info = env.step(
                Action(
                    action_type=ActionType.FLAG_EVIDENCE,
                    document_id=doc_id,
                    evidence_reason=f"Randomly flagged evidence with seed {seed}.",
                )
            )
            if doc_id not in flagged:
                flagged.append(doc_id)
            final_reward = reward

        elif choice == "suspect":
            person = rng.choice(known_people)
            role = rng.choice(list(SuspectRole))
            evidence_ids = flagged[: max(1, min(2, len(flagged)))]
            obs, reward, done, info = env.step(
                Action(
                    action_type=ActionType.IDENTIFY_SUSPECT,
                    person_name=person,
                    person_role=role,
                    evidence_ids=evidence_ids,
                    evidence_reason=f"Random accusation under seed {seed}.",
                )
            )
            final_reward = reward

    if not done:
        scheme = rng.choice(SCHEME_VALUES)
        obs, reward, done, info = env.step(
            Action(
                action_type=ActionType.SUBMIT_REPORT,
                findings={
                    "scheme_type": scheme,
                    "summary": f"Random final report with seed {seed}.",
                },
            )
        )
        final_reward = reward

    return {
        "score": final_reward.score if final_reward else 0.0,
        "breakdown": final_reward.breakdown if final_reward else {},
        "steps": env.state().get("step_count", 0),
        "done": done,
        "seed": seed,
    }


def run_random_policy_summary(task_id: str, seeds: List[int]) -> Dict[str, Any]:
    runs = [run_random_policy_once(task_id, seed) for seed in seeds]
    scores = [r["score"] for r in runs]
    steps = [r["steps"] for r in runs]

    return {
        "score_mean": statistics.mean(scores),
        "score_std": statistics.pstdev(scores) if len(scores) > 1 else 0.0,
        "steps_mean": statistics.mean(steps),
        "runs": runs,
    }


def safe_round(x: float) -> float:
    return round(float(x), 4)


def audit_all() -> Dict[str, Any]:
    task_ids = ["easy", "medium", "hard"]
    results: Dict[str, Dict[str, Any]] = {
        "per_task": {},
        "per_policy": {},
        "meta": {
            "task_ids": task_ids,
            "random_seeds": [0, 1, 2, 3, 4],
        },
    }

    for task_id in task_ids:
        task_results = {}

        task_results["scheme_only_submit"] = run_scheme_only_submit(task_id)
        task_results["read_only_then_submit"] = run_read_only_then_submit(task_id)

        fallback_result = run_fallback_baseline(task_id)
        if fallback_result is not None:
            task_results["submitted_baseline_fallback"] = fallback_result

        task_results["oracle_case"] = run_oracle_case(task_id)
        task_results["false_accusation_case"] = run_false_accusation_case(task_id)
        task_results["overinclusive_case"] = run_overinclusive_case(task_id)
        task_results["random_policy"] = run_random_policy_summary(
            task_id, [0, 1, 2, 3, 4]
        )

        results["per_task"][task_id] = task_results

    # Policy-centric aggregation
    policies = set()
    for task_id in task_ids:
        policies.update(results["per_task"][task_id].keys())

    for policy in sorted(policies):
        per_task_scores = {}
        numeric_scores = []

        for task_id in task_ids:
            task_result = results["per_task"][task_id].get(policy)
            if task_result is None:
                continue

            if policy == "random_policy":
                score = task_result["score_mean"]
            else:
                score = task_result["score"]

            per_task_scores[task_id] = safe_round(score)
            numeric_scores.append(score)

        results["per_policy"][policy] = {
            "scores": per_task_scores,
            "average": safe_round(statistics.mean(numeric_scores))
            if numeric_scores
            else None,
        }

    return results


def markdown_table(results: Dict[str, Any]) -> str:
    policies = list(results["per_policy"].keys())

    lines = []
    lines.append("| Policy | Easy | Medium | Hard | Average |")
    lines.append("|---|---:|---:|---:|---:|")

    for policy in policies:
        row = results["per_policy"][policy]
        scores = row["scores"]
        easy = scores.get("easy", "-")
        medium = scores.get("medium", "-")
        hard = scores.get("hard", "-")
        avg = row["average"]
        lines.append(f"| {policy} | {easy} | {medium} | {hard} | {avg} |")

    return "\n".join(lines)


def build_findings(results: Dict[str, Any]) -> List[str]:
    findings = []
    per_policy = results["per_policy"]

    if "scheme_only_submit" in per_policy:
        findings.append(
            f"- **Scheme-only submit** averages **{per_policy['scheme_only_submit']['average']}**, "
            "showing that guessing the fraud type without evidence is not enough."
        )

    if "read_only_then_submit" in per_policy:
        findings.append(
            f"- **Read-only then submit** averages **{per_policy['read_only_then_submit']['average']}**, "
            "demonstrating that document inspection alone is insufficient unless the agent structures findings."
        )

    if "oracle_case" in per_policy:
        findings.append(
            f"- **Oracle case** averages **{per_policy['oracle_case']['average']}**, "
            "showing the tasks are solvable and the grader rewards correct evidence-grounded behavior."
        )

    if "false_accusation_case" in per_policy and "oracle_case" in per_policy:
        oracle_avg = per_policy["oracle_case"]["average"]
        false_avg = per_policy["false_accusation_case"]["average"]
        findings.append(
            f"- Adding a **false accusation** drops the average from **{oracle_avg}** to **{false_avg}**, "
            "indicating that over-aggressive accusations are meaningfully penalized."
        )

    if "overinclusive_case" in per_policy and "oracle_case" in per_policy:
        over_avg = per_policy["overinclusive_case"]["average"]
        oracle_avg = per_policy["oracle_case"]["average"]
        findings.append(
            f"- **Overinclusive evidence / accusation behavior** scores **{over_avg}** vs oracle **{oracle_avg}**, "
            "suggesting the benchmark values precision over shotgun evidence collection."
        )

    if "random_policy" in per_policy:
        findings.append(
            f"- **Random policy mean** averages **{per_policy['random_policy']['average']}**, "
            "showing that the environment is not trivially exploitable by unguided behavior."
        )

    return findings


def build_markdown_report(results: Dict[str, Any]) -> str:
    findings = build_findings(results)

    md = []
    md.append("# Benchmark Audit")
    md.append("")
    md.append(
        "This document audits the forensic fraud investigation environment for "
        "benchmark validity, exploit resistance, and score calibration."
    )
    md.append("")
    md.append("## Policies evaluated")
    md.append("")
    md.append(
        "- **scheme_only_submit**: immediately submits the correct scheme type without gathering evidence"
    )
    md.append(
        "- **read_only_then_submit**: examines gold-relevant documents but does not flag evidence or build a case"
    )
    md.append(
        "- **submitted_baseline_fallback**: deterministic task-aware baseline report used by the submitted inference fallback path"
    )
    md.append(
        "- **oracle_case**: uses gold evidence, gold perpetrators, and a coherent timeline"
    )
    md.append(
        "- **false_accusation_case**: oracle-like case plus one intentionally wrong accusation"
    )
    md.append(
        "- **overinclusive_case**: oracle-like case plus irrelevant evidence and/or an overinclusive accusation"
    )
    md.append("- **random_policy**: seeded random action policy averaged over 5 runs")
    md.append("")
    md.append("## Score table")
    md.append("")
    md.append(markdown_table(results))
    md.append("")
    md.append("## Key findings")
    md.append("")
    for finding in findings:
        md.append(finding)
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append(
        "The audit is intended to show that the benchmark rewards structured, "
        "evidence-grounded investigation while penalizing under-specified, random, "
        "or overly aggressive case-building behavior."
    )
    md.append("")
    md.append(
        "In particular, the gap between naive and oracle-like policies indicates that "
        "the environment is non-trivial, while the false-accusation and overinclusive "
        "cases probe whether the benchmark values precision and careful attribution."
    )
    md.append("")
    return "\n".join(md)


def print_console_summary(results: Dict[str, Any]):
    print("\n" + "=" * 80)
    print("BENCHMARK AUDIT SUMMARY")
    print("=" * 80)
    print(markdown_table(results))
    print("\nKey findings:")
    for finding in build_findings(results):
        print(finding)

    print("\nPer-task random policy details:")
    for task_id, task_results in results["per_task"].items():
        rp = task_results["random_policy"]
        print(
            f"  {task_id}: mean={safe_round(rp['score_mean'])} "
            f"std={safe_round(rp['score_std'])} "
            f"steps_mean={safe_round(rp['steps_mean'])}"
        )


def main():
    results = audit_all()

    Path(OUTPUT_JSON).write_text(json.dumps(results, indent=2), encoding="utf-8")
    Path(OUTPUT_MD).write_text(build_markdown_report(results), encoding="utf-8")

    print_console_summary(results)
    print(f"\nWrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")


if __name__ == "__main__":
    main()
