from typing import Dict, Any

class ResponseBuilder:
    @staticmethod
    def build_success_response(data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "success",
            "data": {
                "claim_allowed": data.get("claim_allowed"),
                "reason": data.get("reason"),
                "reference_clause": data.get("reference_clause"),
                "confidence_score": round(data.get("confidence_score", 0.0), 2)
            }
        }

    @staticmethod
    def build_error_response(error_message: str) -> Dict[str, Any]:
        return {
            "status": "error",
            "message": error_message
        }
