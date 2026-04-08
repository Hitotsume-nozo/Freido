from typing import Dict, List, Any, Optional
from models import Suspect, SuspectRole, FlaggedItem, TimelineEvent


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

        # Positive components
        perp_score = self._grade_perpetrators(identified_suspects)
        scheme_score = self._grade_scheme(scheme_type)
        evidence_score = self._grade_evidence(flagged_evidence)
        timeline_score = self._grade_timeline(timeline)

        breakdown["perpetrators"] = perp_score
        breakdown["scheme_type"] = scheme_score
        breakdown["evidence"] = evidence_score
        breakdown["timeline"] = timeline_score

        positive_total = perp_score + scheme_score + evidence_score + timeline_score

        # IMPORTANT:
        # Clamp positive part first so penalties are never hidden by overflow > 1.0
        positive_total_capped = min(1.0, positive_total)

        penalty = self._false_accusation_penalty(identified_suspects)
        breakdown["false_accusation_penalty"] = -penalty

        final_score = max(0.0, min(1.0, positive_total_capped - penalty))

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
            all_names = {name.lower(), *(a.lower() for a in aliases)}

            for suspect in suspects:
                if suspect.name.lower() in all_names:
                    if self._role_matches(suspect.role, info["role"]):
                        score += weight
                    else:
                        # Partial credit for naming the right person but wrong role
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

        clean_given = scheme_type.lower().replace(" ", "_")
        clean_expected = expected.lower().replace(" ", "_")

        if clean_given == clean_expected:
            return weight

        related = {
            "revenue_fabrication": [
                "financial_fraud",
                "accounting_fraud",
                "revenue_fraud",
            ],
            "expense_fraud": ["expense_report_fraud", "fake_expenses"],
            "vendor_kickback": ["procurement_fraud", "kickback", "vendor_fraud"],
        }

        if clean_given in related.get(clean_expected, []):
            return weight * 0.5

        return 0.0

    def _grade_evidence(self, flagged: List[FlaggedItem]) -> float:
        score = 0.0
        gold_evidence = self.gold.get("key_evidence", {})
        flagged_ids = {item.document_id for item in flagged}

        for doc_id, info in gold_evidence.items():
            if doc_id in flagged_ids:
                score += info["weight"]

        # Small anti-spam penalty for irrelevant flagged evidence
        wrong_flags = [doc_id for doc_id in flagged_ids if doc_id not in gold_evidence]
        score -= min(0.10, 0.01 * len(wrong_flags))

        return max(0.0, score)

    def _false_accusation_penalty(self, suspects: List[Suspect]) -> float:
        """
        Stronger and more realistic penalty design:
        - accusing a known innocent as mastermind/accomplice hurts a lot
        - accusing a witness/participant as mastermind/accomplice hurts moderately
        - inventing unknown suspects hurts moderately
        - correct suspect but wrong role is already handled by partial credit, so no extra penalty
        """
        base_penalty = self.gold.get("false_accusation_penalty", 0.10)

        gold_perps = self.gold.get("perpetrators", {})
        non_perps = self.gold.get("non_perpetrators", {})

        gold_name_to_info = {}
        for name, info in gold_perps.items():
            gold_name_to_info[name.lower()] = info
            for alias in info.get("aliases", []):
                gold_name_to_info[alias.lower()] = info

        non_perp_name_to_info = {name.lower(): info for name, info in non_perps.items()}

        penalty = 0.0

        for suspect in suspects:
            sname = suspect.name.lower()
            srole = suspect.role.value

            # Correct perpetrators: no accusation penalty here
            if sname in gold_name_to_info:
                continue

            # Known non-perp
            if sname in non_perp_name_to_info:
                info = non_perp_name_to_info[sname]
                true_role = info.get("role")
                acceptable_roles = info.get("acceptable_roles", [])

                # If explicitly acceptable, no penalty
                if acceptable_roles and srole in acceptable_roles:
                    continue

                # Innocent person wrongly accused as perpetrator = heavy penalty
                if true_role == "innocent":
                    if srole in ["mastermind", "accomplice"]:
                        penalty += base_penalty * 1.25
                    elif srole == "reluctant_participant":
                        penalty += base_penalty * 0.75
                    else:
                        penalty += base_penalty * 0.40
                    continue

                # Witness / non-perp wrongly promoted to perpetrator = moderate penalty
                if true_role in ["witness", "reluctant_participant"]:
                    if srole in ["mastermind", "accomplice"]:
                        penalty += base_penalty * 0.80
                    elif (
                        srole == "reluctant_participant"
                        and true_role != "reluctant_participant"
                    ):
                        penalty += base_penalty * 0.35
                    elif srole == "witness":
                        penalty += base_penalty * 0.10
                    continue

                # Fallback for any other known non-perp category
                penalty += base_penalty * 0.50
                continue

            # Unknown fabricated suspect = moderate penalty
            if srole in ["mastermind", "accomplice"]:
                penalty += base_penalty * 0.70
            elif srole == "reluctant_participant":
                penalty += base_penalty * 0.45
            else:
                penalty += base_penalty * 0.25

        # Cap total penalty but allow it to matter strongly
        return min(penalty, 0.35)

    def _grade_timeline(self, timeline: List[TimelineEvent]) -> float:
        if not timeline:
            return 0.0

        weight = self.gold.get("timeline_weight", 0.10)

        if len(timeline) >= 3:
            return weight
        elif len(timeline) >= 1:
            return weight * 0.5
        return 0.0

    def _build_message(self, breakdown: Dict[str, float], final: float) -> str:
        parts = []
        for key, val in breakdown.items():
            parts.append(f"{key}: {val:+.4f}")
        return f"Final score: {final:.4f} | " + " | ".join(parts)
