# graders.py
from typing import Dict, List, Any, Optional
from models import (
    Suspect,
    SuspectRole,
    SchemeType,
    FlaggedItem,
    TimelineEvent,
    FindingsReport,
)


class FraudInvestigationGrader:
    """Deterministic grader for fraud investigation tasks."""

    def __init__(self, gold_labels: Dict[str, Any]):
        self.gold = gold_labels

    def grade(
        self,
        identified_suspects: List[Suspect],
        flagged_evidence: List[FlaggedItem],
        scheme_type: Optional[str],
        timeline: List[TimelineEvent],
        findings: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        breakdown = {}
        total = 0.0

        # 1. Perpetrator identification
        perp_score = self._grade_perpetrators(identified_suspects)
        breakdown["perpetrators"] = perp_score
        total += perp_score

        # 2. Scheme identification
        scheme_score = self._grade_scheme(scheme_type)
        breakdown["scheme_type"] = scheme_score
        total += scheme_score

        # 3. Evidence collection
        evidence_score = self._grade_evidence(flagged_evidence)
        breakdown["evidence"] = evidence_score
        total += evidence_score

        # 4. False accusation penalty
        penalty = self._false_accusation_penalty(identified_suspects)
        breakdown["false_accusation_penalty"] = -penalty
        total -= penalty

        # 5. Timeline accuracy
        timeline_score = self._grade_timeline(timeline)
        breakdown["timeline"] = timeline_score
        total += timeline_score

        final_score = max(0.0, min(1.0, total))

        return {
            "score": round(final_score, 4),
            "breakdown": {k: round(v, 4) for k, v in breakdown.items()},
            "message": self._build_message(breakdown, final_score),
        }

    def _grade_perpetrators(self, suspects: List[Suspect]) -> float:
        score = 0.0
        gold_perps = self.gold.get("perpetrators", {})

        for name, info in gold_perps.items():
            weight = info["weight"]
            aliases = info.get("aliases", [])
            all_names = [name.lower()] + [a.lower() for a in aliases]

            for suspect in suspects:
                if suspect.name.lower() in all_names:
                    # Full credit for correct name
                    role_match = self._role_matches(suspect.role, info["role"])
                    if role_match:
                        score += weight
                    else:
                        # Half credit for correct person, wrong role
                        score += weight * 0.5
                    break

        return score

    def _role_matches(self, given: SuspectRole, expected: str) -> bool:
        return given.value == expected

    def _grade_scheme(self, scheme_type: Optional[str]) -> float:
        if scheme_type is None:
            return 0.0
        expected = self.gold.get("scheme_type", "")
        weight = self.gold.get("scheme_weight", 0.15)
        if scheme_type.lower().replace(" ", "_") == expected.lower():
            return weight
        # Partial credit for related schemes
        related = {
            "revenue_fabrication": [
                "financial_fraud",
                "accounting_fraud",
                "revenue_fraud",
            ],
            "expense_fraud": ["expense_report_fraud", "fake_expenses"],
            "vendor_kickback": ["procurement_fraud", "kickback", "vendor_fraud"],
        }
        related_terms = related.get(expected, [])
        clean_given = scheme_type.lower().replace(" ", "_")
        if clean_given in related_terms:
            return weight * 0.5
        return 0.0

    def _grade_evidence(self, flagged: List[FlaggedItem]) -> float:
        score = 0.0
        gold_evidence = self.gold.get("key_evidence", {})
        flagged_ids = {item.document_id for item in flagged}

        for doc_id, info in gold_evidence.items():
            if doc_id in flagged_ids:
                score += info["weight"]

        return score

    def _false_accusation_penalty(self, suspects: List[Suspect]) -> float:
        penalty_per = self.gold.get("false_accusation_penalty", 0.10)
        gold_perps = self.gold.get("perpetrators", {})
        non_perps = self.gold.get("non_perpetrators", {})

        penalty = 0.0
        gold_names = set()
        for name in gold_perps:
            gold_names.add(name.lower())
            for alias in gold_perps[name].get("aliases", []):
                gold_names.add(alias.lower())

        acceptable_names = set()
        for name, info in non_perps.items():
            acceptable_roles = info.get("acceptable_roles", [])
            if acceptable_roles:
                acceptable_names.add(name.lower())

        for suspect in suspects:
            sname = suspect.name.lower()
            if sname in gold_names:
                continue
            if sname in acceptable_names:
                # Check if role is acceptable
                non_perp_info = None
                for npname, npinfo in non_perps.items():
                    if npname.lower() == sname:
                        non_perp_info = npinfo
                        break
                if non_perp_info:
                    acceptable = non_perp_info.get("acceptable_roles", [])
                    if suspect.role.value in acceptable:
                        continue
            # Check if truly innocent
            if sname in {n.lower() for n in non_perps}:
                non_perp_info = non_perps.get(
                    next(n for n in non_perps if n.lower() == sname), {}
                )
                if non_perp_info.get("role") == "innocent":
                    penalty += penalty_per
                else:
                    # Not innocent but wrongly accused as perpetrator
                    if suspect.role in [SuspectRole.MASTERMIND, SuspectRole.ACCOMPLICE]:
                        penalty += penalty_per * 0.5

        return penalty

    def _grade_timeline(self, timeline: List[TimelineEvent]) -> float:
        if not timeline:
            return 0.0
        weight = self.gold.get("timeline_weight", 0.10)
        # Give credit for having a timeline with reasonable events
        if len(timeline) >= 3:
            return weight
        elif len(timeline) >= 1:
            return weight * 0.5
        return 0.0

    def _build_message(self, breakdown: Dict, final: float) -> str:
        parts = []
        for key, val in breakdown.items():
            parts.append(f"{key}: {val:+.4f}")
        return f"Final score: {final:.4f} | " + " | ".join(parts)
