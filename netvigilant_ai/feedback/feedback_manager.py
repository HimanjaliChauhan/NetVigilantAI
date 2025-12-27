import pandas as pd
from pathlib import Path

class FeedbackManager:
    """
    Handles user feedback and tracks false positives.
    """

    def __init__(self):
        self.log_path = Path("feedback_log.csv")

    def record_feedback(self, row, label):
        entry = {
            "timestamp": row["timestamp"],
            "source_id": row["source_id"],
            "anomaly_score": row["anomaly_score"],
            "user_label": label
        }

        df = pd.DataFrame([entry])

        if self.log_path.exists():
            df.to_csv(self.log_path, mode="a", header=False, index=False)
        else:
            df.to_csv(self.log_path, index=False)

    def get_false_positive_rate(self):
        if not self.log_path.exists():
            return 0.0

        df = pd.read_csv(self.log_path)
        if df.empty:
            return 0.0

        return (df["user_label"] == "False Positive").mean()
