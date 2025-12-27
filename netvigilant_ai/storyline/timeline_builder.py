import pandas as pd


class AttackTimelineBuilder:
    """
    Builds attack timelines per source_id
    based on anomaly progression over time.
    """

    def __init__(self):
        pass

    def build_timelines(self, df: pd.DataFrame) -> dict:
        """
        Returns timelines grouped by source_id.
        Each timeline is a list of ordered events.
        """

        timelines = {}

        # Ensure chronological order
        df_sorted = df.sort_values("timestamp")

        for source_id, group in df_sorted.groupby("source_id"):
            events = []

            for _, row in group.iterrows():
                if row["is_anomaly"]:
                    stage = self._determine_stage(row["anomaly_score"])
                    events.append({
                        "timestamp": row["timestamp"],
                        "stage": stage,
                        "anomaly_score": int(row["anomaly_score"])
                    })

            if events:
                timelines[source_id] = events

        return timelines

    def _determine_stage(self, anomaly_score: int) -> str:
        """
        Maps anomaly strength to attack stage.
        """
        if anomaly_score == 1:
            return "Suspicious Activity"
        elif anomaly_score == 2:
            return "Potential Attack"
        else:
            return "Confirmed Attack"
