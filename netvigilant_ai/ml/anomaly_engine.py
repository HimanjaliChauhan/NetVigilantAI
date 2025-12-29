import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler


class AnomalyDetectionEngine:
    """
    Explainable Network Anomaly Detection Engine

    Models Used:
    - Isolation Forest
    - Local Outlier Factor (LOF)

    Output:
    - anomaly_score (0, 1, 2)
    - is_anomaly (True / False)
    """

    def __init__(self):
        self.scaler = StandardScaler()

        self.iforest = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )

        self.lof = LocalOutlierFactor(
            n_neighbors=20,
            contamination=0.05,
            novelty=True
        )

    # -------------------------
    # MAIN PIPELINE
    # -------------------------
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Runs the full anomaly detection pipeline.
        This is the ONLY method the dashboard should call.
        """

        # Required numeric features
        feature_cols = [
            "duration",
            "src_bytes",
            "dst_bytes",
            "count",
            "srv_count"
        ]

        # Validate columns
        for col in feature_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Feature matrix
        X = df[feature_cols].values
        X_scaled = self.scaler.fit_transform(X)

        # -------------------------
        # Isolation Forest
        # -------------------------
        if_predictions = self.iforest.fit_predict(X_scaled)
        if_scores = (if_predictions == -1).astype(int)

        # -------------------------
        # Local Outlier Factor
        # -------------------------
        self.lof.fit(X_scaled)
        lof_predictions = self.lof.predict(X_scaled)
        lof_scores = (lof_predictions == -1).astype(int)

        # -------------------------
        # Final Ensemble Score
        # -------------------------
        anomaly_score = if_scores + lof_scores

        # -------------------------
        # Build result dataframe
        # -------------------------
        df_result = df.copy()
        df_result["iforest_flag"] = if_scores
        df_result["lof_flag"] = lof_scores
        df_result["anomaly_score"] = anomaly_score
        df_result["is_anomaly"] = df_result["anomaly_score"] >= 1

        # -------------------------
        # Explainability statistics
        # -------------------------
        for col in ["src_bytes", "dst_bytes", "count", "srv_count"]:
            df_result[f"{col}_mean"] = df[col].mean()
            df_result[f"{col}_zscore"] = (
                (df[col] - df[col].mean()) / (df[col].std() + 1e-6)
            )

        return df_result
