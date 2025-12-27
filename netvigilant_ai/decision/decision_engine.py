from datetime import datetime

class DecisionEngine:
    """
    Simulates response actions for anomalies.
    No real enforcement is performed.
    """

    def simulate_decision(self, row, decision):
        impact_map = {
            "Ignore": "No action taken. Possible risk if anomaly is real.",
            "Monitor": "Traffic will be closely observed for escalation.",
            "Quarantine": "Source would be isolated (simulation only)."
        }

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "source_id": row["source_id"],
            "decision": decision,
            "predicted_impact": impact_map.get(decision, "Unknown")
        }
