import pandas as pd


class AnomalyExplainer:
    """
    Generates human-readable explanations
    for detected network anomalies.
    """

    def __init__(self):
        pass

    def explain_row(self, row: pd.Series) -> str:
        reasons = []

        # Feature-based explanations
        if row["src_bytes"] > row["src_bytes_mean"]:
            reasons.append("high volume of data sent from source")

        if row["dst_bytes"] > row["dst_bytes_mean"]:
            reasons.append("high volume of data received by destination")

        if row["count"] > row["count_mean"]:
            reasons.append("repeated connection attempts")

        if row["srv_count"] > row["srv_count_mean"]:
            reasons.append("multiple connections to the same service")

        # Model agreement explanation
        model_votes = row["anomaly_score"]

        if model_votes == 3:
            model_text = "all detection models agreed"
        elif model_votes == 2:
            model_text = "multiple detection models agreed"
        else:
            model_text = "a single detection model flagged this behavior"

        if not reasons:
            reasons.append("overall behavior deviated from normal patterns")

        explanation = (
            f"This network session was flagged because it showed "
            f"{', '.join(reasons)}. "
            f"Additionally, {model_text} that this activity is anomalous."
        )

        return explanation
