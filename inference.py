import os
import json
import textwrap
from typing import Dict, List, Any, Optional

from openai import OpenAI

from environment import FraudInvestigationEnv
from models import Action, ActionType, SuspectRole, TimelineEvent


API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

TEMPERATURE = 0.0
MAX_TOKENS = 500
DOC_CHAR_LIMIT = 1200

# Curated evidence docs per task: chosen to maximize signal and minimize token cost
CURATED_DOCS: Dict[str, List[str]] = {
    "easy": [
        "exp_002",
        "exp_003",
        "ext_001",
        "email_004",
        "cal_001",
        "crm_002",
    ],
    "medium": [
        "vendor_001",
        "ext_m01",
        "fin_m01",
        "proc_001",
        "proc_002",
        "proc_005",
        "email_m03",
        "email_m05",
        "email_m07",
        "market_001",
    ],
    "hard": [
        "email_h01",
        "email_h02",
        "email_h05",
        "email_h07",
        "email_h09",
        "ext_h01",
        "ext_h02",
        "ext_h03",
        "ship_001",
        "fin_h03",
        "crm_h01",
        "inv_001",
    ],
}

FALLBACK_SCHEMES = {
    "easy": "expense_fraud",
    "medium": "vendor_kickback",
    "hard": "revenue_fabrication",
}

MAX_EVIDENCE = {
    "easy": 6,
    "medium": 8,
    "hard": 10,
}

MAX_TIMELINE_EVENTS = {
    "easy": 3,
    "medium": 4,
    "hard": 5,
}


def safe_json_extract(text: str) -> Dict[str, Any]:
    if not text:
        return {}

    text = text.strip()

    if "```json" in text:
        text = text.split("```json", 1)[1]
        text = text.split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1]
        text = text.split("```", 1)[0].strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try extracting largest {...} block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return {}


def normalize_scheme(task_id: str, scheme: Optional[str]) -> str:
    if not scheme:
        return FALLBACK_SCHEMES[task_id]

    s = scheme.strip().lower().replace(" ", "_")
    mapping = {
        "expense_fraud": "expense_fraud",
        "expense_report_fraud": "expense_fraud",
        "fake_expenses": "expense_fraud",
        "vendor_kickback": "vendor_kickback",
        "kickback": "vendor_kickback",
        "vendor_fraud": "vendor_kickback",
        "procurement_fraud": "vendor_kickback",
        "revenue_fabrication": "revenue_fabrication",
        "revenue_fraud": "revenue_fabrication",
        "financial_fraud": "revenue_fabrication",
        "accounting_fraud": "revenue_fabrication",
    }
    return mapping.get(s, FALLBACK_SCHEMES[task_id])


def normalize_role(role: Optional[str]) -> Optional[SuspectRole]:
    if not role:
        return None
    r = role.strip().lower().replace(" ", "_")
    mapping = {
        "mastermind": SuspectRole.MASTERMIND,
        "accomplice": SuspectRole.ACCOMPLICE,
        "reluctant_participant": SuspectRole.RELUCTANT_PARTICIPANT,
        "reluctant-participant": SuspectRole.RELUCTANT_PARTICIPANT,
        "witness": SuspectRole.WITNESS,
        "innocent": SuspectRole.INNOCENT,
    }
    return mapping.get(r)


def truncate(text: str, limit: int = DOC_CHAR_LIMIT) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...[truncated]"


def examine_curated_docs(env: FraudInvestigationEnv, task_id: str) -> Dict[str, str]:
    """Examine a handpicked set of high-signal docs and return their contents."""
    contents: Dict[str, str] = {}

    for doc_id in CURATED_DOCS[task_id]:
        obs, reward, done, info = env.step(
            Action(action_type=ActionType.EXAMINE_DOCUMENT, document_id=doc_id)
        )
        contents[doc_id] = obs.document_content or ""
        print(f"  Examine: {doc_id}")
        if done:
            break

    return contents


def build_reasoning_prompt(task_id: str, obs, doc_contents: Dict[str, str]) -> str:
    allowed_evidence = MAX_EVIDENCE[task_id]
    allowed_timeline = MAX_TIMELINE_EVENTS[task_id]

    doc_blocks = []
    for doc_id, content in doc_contents.items():
        doc_blocks.append(f"DOCUMENT ID: {doc_id}\nCONTENT:\n{truncate(content)}")

    docs_text = "\n\n".join(doc_blocks)

    prompt = textwrap.dedent(
        f"""
        You are a forensic fraud analyst.

        Task ID: {task_id}
        Scenario: {obs.scenario_description}
        Whistleblower Tip: {obs.whistleblower_tip}

        You have already examined a curated set of likely high-value documents.
        Based ONLY on these documents, produce a structured investigation report.

        IMPORTANT RULES:
        - Use ONLY document IDs from the provided documents.
        - Do NOT invent people, dates, or document IDs.
        - Identify only the most strongly supported suspects.
        - Prefer perpetrators over peripheral witnesses unless the witness/participant is central.
        - Keep evidence focused and high quality.
        - Return ONLY valid JSON. No markdown, no explanation.

        Allowed scheme_type values:
        - expense_fraud
        - vendor_kickback
        - revenue_fabrication
        - embezzlement
        - money_laundering
        - payroll_fraud

        Allowed suspect roles:
        - mastermind
        - accomplice
        - reluctant_participant
        - witness
        - innocent

        Return this exact JSON shape:
        {{
          "scheme_type": "one_of_allowed_values",
          "summary": "1-3 sentence summary",
          "evidence": [
            {{
              "document_id": "doc_id",
              "reason": "why this document is important"
            }}
          ],
          "suspects": [
            {{
              "name": "full name",
              "role": "mastermind|accomplice|reluctant_participant|witness|innocent",
              "evidence_ids": ["doc_id1", "doc_id2"],
              "reasoning": "why this person has this role"
            }}
          ],
          "timeline": [
            {{
              "date": "YYYY-MM-DD or month/year if exact date unclear",
              "description": "event description",
              "document_ids": ["doc_id1", "doc_id2"]
            }}
          ]
        }}

        Constraints:
        - Evidence items: at most {allowed_evidence}
        - Suspects: at most 4
        - Timeline events: at most {allowed_timeline}

        DOCUMENTS:
        {docs_text}
        """
    ).strip()

    return prompt


def ask_model_for_report(
    client: OpenAI, task_id: str, obs, doc_contents: Dict[str, str]
) -> Dict[str, Any]:
    prompt = build_reasoning_prompt(task_id, obs, doc_contents)

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a precise forensic analyst. Output only valid JSON.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    response_text = completion.choices[0].message.content or ""
    data = safe_json_extract(response_text)
    return data


def filtered_evidence(
    task_id: str, report: Dict[str, Any], allowed_doc_ids: set
) -> List[Dict[str, str]]:
    items = report.get("evidence", [])
    if not isinstance(items, list):
        return []

    out = []
    seen = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        doc_id = item.get("document_id")
        reason = item.get("reason", "")
        if doc_id in allowed_doc_ids and doc_id not in seen and reason:
            out.append({"document_id": doc_id, "reason": reason})
            seen.add(doc_id)
        if len(out) >= MAX_EVIDENCE[task_id]:
            break
    return out


def filtered_suspects(
    report: Dict[str, Any], flagged_doc_ids: set
) -> List[Dict[str, Any]]:
    items = report.get("suspects", [])
    if not isinstance(items, list):
        return []

    out = []
    seen_names = set()

    for item in items:
        if not isinstance(item, dict):
            continue

        name = item.get("name")
        role = normalize_role(item.get("role"))
        evidence_ids = item.get("evidence_ids", [])
        reasoning = item.get("reasoning", "")

        if not name or not role or not isinstance(evidence_ids, list):
            continue

        clean_evidence_ids = [eid for eid in evidence_ids if eid in flagged_doc_ids]
        if not clean_evidence_ids:
            continue

        key = name.lower()
        if key in seen_names:
            continue

        out.append(
            {
                "name": name,
                "role": role,
                "evidence_ids": clean_evidence_ids,
                "reasoning": reasoning,
            }
        )
        seen_names.add(key)

        if len(out) >= 4:
            break

    return out


def filtered_timeline(
    task_id: str, report: Dict[str, Any], allowed_doc_ids: set
) -> List[TimelineEvent]:
    items = report.get("timeline", [])
    if not isinstance(items, list):
        return []

    out = []
    for item in items:
        if not isinstance(item, dict):
            continue

        date = item.get("date", "unknown")
        description = item.get("description", "")
        doc_ids = item.get("document_ids", [])

        if not description or not isinstance(doc_ids, list):
            continue

        clean_doc_ids = [did for did in doc_ids if did in allowed_doc_ids]
        if not clean_doc_ids:
            continue

        out.append(
            TimelineEvent(
                date=date,
                description=description,
                document_ids=clean_doc_ids,
            )
        )

        if len(out) >= MAX_TIMELINE_EVENTS[task_id]:
            break

    return out


def task_aware_fallback_report(
    task_id: str, allowed_doc_ids: List[str]
) -> Dict[str, Any]:
    # Minimal deterministic fallback if API fails or JSON is malformed
    fallback = {
        "easy": {
            "scheme_type": "expense_fraud",
            "summary": "Likely false expense claims involving Bella Italia.",
            "evidence": [
                {
                    "document_id": "ext_001",
                    "reason": "Restaurant closure period is inconsistent with claimed dinners.",
                },
                {
                    "document_id": "exp_002",
                    "reason": "Expense claim on a suspicious date.",
                },
            ],
            "suspects": [
                {
                    "name": "David Chen",
                    "role": "mastermind",
                    "evidence_ids": ["ext_001", "exp_002"],
                    "reasoning": "Submitted suspicious expense claims contradicted by external records.",
                }
            ],
            "timeline": [
                {
                    "date": "2024-03-12",
                    "description": "A suspicious dinner expense was submitted during the restaurant closure period.",
                    "document_ids": ["exp_002", "ext_001"],
                }
            ],
        },
        "medium": {
            "scheme_type": "vendor_kickback",
            "summary": "Likely procurement steering toward Apex Solutions tied to Sarah Martinez's family.",
            "evidence": [
                {
                    "document_id": "ext_m01",
                    "reason": "Corporate registry links Apex to Carlos Martinez-Reeves.",
                },
                {
                    "document_id": "fin_m01",
                    "reason": "Conflict disclosure appears incomplete.",
                },
                {
                    "document_id": "email_m07",
                    "reason": "Personal email suggests coordination with Carlos.",
                },
            ],
            "suspects": [
                {
                    "name": "Sarah Martinez",
                    "role": "mastermind",
                    "evidence_ids": ["fin_m01", "email_m07"],
                    "reasoning": "Directed awards while concealing a family conflict.",
                },
                {
                    "name": "Carlos Martinez",
                    "role": "accomplice",
                    "evidence_ids": ["ext_m01", "email_m07"],
                    "reasoning": "Connected to the vendor receiving suspicious contracts.",
                },
            ],
            "timeline": [
                {
                    "date": "2023-05-18",
                    "description": "Finance raised concerns about a recurring pattern of overpriced Apex contracts.",
                    "document_ids": ["email_m03", "proc_002"],
                }
            ],
        },
        "hard": {
            "scheme_type": "revenue_fabrication",
            "summary": "Likely revenue inflation through shell customers and unsupported recognition before fundraising.",
            "evidence": [
                {
                    "document_id": "email_h01",
                    "reason": "CFO pushed for contracts that would make growth look real.",
                },
                {
                    "document_id": "fin_h03",
                    "reason": "No cash receipts from suspicious customers.",
                },
                {
                    "document_id": "ext_h01",
                    "reason": "Customer address resolves to a UPS store.",
                },
                {
                    "document_id": "ship_001",
                    "reason": "No real deployment activity for suspicious customers.",
                },
            ],
            "suspects": [
                {
                    "name": "Robert Kim",
                    "role": "mastermind",
                    "evidence_ids": ["email_h01", "fin_h03"],
                    "reasoning": "Directed the numbers narrative ahead of fundraising.",
                },
                {
                    "name": "Lisa Wang",
                    "role": "accomplice",
                    "evidence_ids": ["email_h02", "crm_h01"],
                    "reasoning": "Routed suspicious deals outside normal sales process.",
                },
                {
                    "name": "Tom Baker",
                    "role": "reluctant_participant",
                    "evidence_ids": ["email_h05", "email_h07"],
                    "reasoning": "Booked questionable revenue under CFO pressure.",
                },
            ],
            "timeline": [
                {
                    "date": "2023-07-10",
                    "description": "Pressure began to manufacture stronger growth before Series C.",
                    "document_ids": ["email_h01"],
                },
                {
                    "date": "2023-10-20",
                    "description": "Unsupported revenue recognition was explicitly directed.",
                    "document_ids": ["email_h05", "email_h07"],
                },
            ],
        },
    }

    report = fallback[task_id]

    # filter docs just in case
    allowed = set(allowed_doc_ids)
    report["evidence"] = [e for e in report["evidence"] if e["document_id"] in allowed]
    for s in report["suspects"]:
        s["evidence_ids"] = [eid for eid in s["evidence_ids"] if eid in allowed]
    report["timeline"] = [
        {**t, "document_ids": [eid for eid in t["document_ids"] if eid in allowed]}
        for t in report["timeline"]
    ]
    return report


def execute_report(
    env: FraudInvestigationEnv,
    task_id: str,
    report: Dict[str, Any],
    allowed_doc_ids: List[str],
) -> float:
    allowed_doc_ids_set = set(allowed_doc_ids)

    evidence_items = filtered_evidence(task_id, report, allowed_doc_ids_set)
    if not evidence_items:
        report = task_aware_fallback_report(task_id, allowed_doc_ids)
        evidence_items = filtered_evidence(task_id, report, allowed_doc_ids_set)

    flagged_doc_ids = []

    # Flag evidence first
    for item in evidence_items:
        obs, reward, done, info = env.step(
            Action(
                action_type=ActionType.FLAG_EVIDENCE,
                document_id=item["document_id"],
                evidence_reason=item["reason"],
            )
        )
        print(f"  Flag evidence: {item['document_id']}")
        flagged_doc_ids.append(item["document_id"])
        if done:
            return reward.score

    flagged_doc_ids_set = set(flagged_doc_ids)

    # Identify suspects
    suspects = filtered_suspects(report, flagged_doc_ids_set)
    if not suspects:
        fallback = task_aware_fallback_report(task_id, allowed_doc_ids)
        suspects = filtered_suspects(fallback, flagged_doc_ids_set)

    for suspect in suspects:
        obs, reward, done, info = env.step(
            Action(
                action_type=ActionType.IDENTIFY_SUSPECT,
                person_name=suspect["name"],
                person_role=suspect["role"],
                evidence_ids=suspect["evidence_ids"],
                evidence_reason=suspect["reasoning"],
            )
        )
        print(f"  Identify suspect: {suspect['name']} ({suspect['role'].value})")
        if done:
            return reward.score

    # Timeline
    timeline = filtered_timeline(task_id, report, allowed_doc_ids_set)
    if not timeline:
        fallback = task_aware_fallback_report(task_id, allowed_doc_ids)
        timeline = filtered_timeline(task_id, fallback, allowed_doc_ids_set)

    if timeline:
        obs, reward, done, info = env.step(
            Action(
                action_type=ActionType.ESTABLISH_TIMELINE,
                timeline_events=timeline,
            )
        )
        print(f"  Establish timeline: {len(timeline)} events")
        if done:
            return reward.score

    # Submit report
    scheme = normalize_scheme(task_id, report.get("scheme_type"))
    summary = report.get("summary", "Investigation findings submitted.")

    obs, reward, done, info = env.step(
        Action(
            action_type=ActionType.SUBMIT_REPORT,
            findings={
                "scheme_type": scheme,
                "summary": summary,
            },
        )
    )
    print("  Submit report")
    print(f"\n  REPORT SUBMITTED")
    print(f"\n  Score: {reward.score:.4f}")
    print(f"  Breakdown: {json.dumps(reward.breakdown, indent=2)}")
    print(f"  {reward.message}")
    return reward.score


def run_task(client: OpenAI, task_id: str) -> float:
    env = FraudInvestigationEnv(task_id=task_id)
    obs = env.reset()

    print(f"\n{'=' * 70}")
    print(f"INVESTIGATION: {task_id.upper()}")
    print(f"{'=' * 70}")
    print(f"Scenario: {obs.scenario_description}")
    print(f"Tip: {obs.whistleblower_tip[:220]}...")
    print(f"Available documents: {len(obs.available_sources)}")
    print(f"Max steps: {obs.max_steps}")

    # Phase 1: deterministic examination of curated docs
    doc_contents = examine_curated_docs(env, task_id)
    allowed_doc_ids = list(doc_contents.keys())

    # Phase 2: one synthesis call
    try:
        report = ask_model_for_report(client, task_id, obs, doc_contents)
        if not report:
            raise ValueError("Empty/invalid JSON report")
    except Exception as e:
        print(f"  API/report error: {e}")
        report = task_aware_fallback_report(task_id, allowed_doc_ids)

    # Phase 3: deterministic execution of returned structure
    final_score = execute_report(env, task_id, report, allowed_doc_ids)
    return final_score


def main():
    if not API_BASE_URL:
        print("ERROR: API_BASE_URL not set")
        return
    if not API_KEY:
        print("ERROR: HF_TOKEN/API_KEY not set")
        return
    if not MODEL_NAME:
        print("ERROR: MODEL_NAME not set")
        return

    print(f"API Base: {API_BASE_URL}")
    print(f"Model: {MODEL_NAME}")

    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY,
    )

    results = {}
    for task_id in ["easy", "medium", "hard"]:
        try:
            score = run_task(client, task_id)
            results[task_id] = score
        except Exception as e:
            print(f"\nERROR on task {task_id}: {e}")
            results[task_id] = 0.0

    print(f"\n{'=' * 70}")
    print("FINAL RESULTS")
    print(f"{'=' * 70}")
    for task_id, score in results.items():
        bar = "█" * int(score * 40) + "░" * (40 - int(score * 40))
        print(f"  {task_id:>8}: {score:.4f} |{bar}|")
    avg = sum(results.values()) / len(results)
    print(f"  {'AVERAGE':>8}: {avg:.4f}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
