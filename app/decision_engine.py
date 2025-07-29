from app.clause_matcher import ClauseMatcher
from typing import Dict

class DecisionEngine:
    def __init__(self, clause_matcher: ClauseMatcher):
        self.matcher = clause_matcher

    def evaluate_claim(self, user_query: str, metadata: Dict) -> Dict:
        """
        metadata can contain keys like:
            - age
            - condition
            - city
            - policy_duration
            - existing_conditions
        """
        result = self.matcher.match_query(user_query)

        if not result.get("match_found"):
            return {
                "claim_allowed": False,
                "reason": result.get("reason", "No clause matched."),
                "reference_clause": result.get("reference_clause", "N/A"),
                "confidence_score": result.get("confidence_score", 0.0)
            }

        clause = result["reference_clause"].lower()

        # Custom business logic examples
        if "30-day waiting period" in clause:
            if metadata.get("policy_duration", 0) < 30:
                return {
                    "claim_allowed": False,
                    "reason": "The policy has a 30-day waiting period, and your policy duration is shorter.",
                    "reference_clause": clause,
                    "confidence_score": result["confidence_score"]
                }

        if "pre-existing" in clause:
            if metadata.get("existing_conditions", False):
                return {
                    "claim_allowed": False,
                    "reason": "Claim rejected due to pre-existing conditions clause.",
                    "reference_clause": clause,
                    "confidence_score": result["confidence_score"]
                }

        # Default: claim allowed
        return {
            "claim_allowed": True,
            "reason": "Query matches clause, and no violations found.",
            "reference_clause": clause,
            "confidence_score": result["confidence_score"]
        }
