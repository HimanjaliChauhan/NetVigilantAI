import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler




class AnomalyDetectionEngine:
    """
    ML Ensemble for Network Anomaly Detection
    Models:
    - Isolation Forest
    - Local Outlier Factor
    - Autoencoder
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

        self.autoencoder = None

    # -------------------------
    # Autoencoder builder
    # -------------------------
    def _build_autoencoder(self, input_dim):
        input_layer = Input(shape=(input_dim,))
        encoded = Dense(8, activation="relu")(input_layer)
        decoded = Dense(input_dim, activation="linear")(encoded)

        autoencoder = Model(input_layer, decoded)
        autoencoder.compile(
            optimizer=Adam(learning_rate=0.001),
            loss="mse"
        )
        return autoencoder

    # -------------------------
    # MAIN ENTRY POINT
    # -------------------------
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Runs full anomaly detection pipeline.
        This is the ONLY method the dashboard should call.
        """

        feature_cols = [
            "duration",
            "src_bytes",
            "dst_bytes",
            "count",
            "srv_count"
        ]

        X = df[feature_cols].values
        X_scaled = self.scaler.fit_transform(X)

        # Isolation Forest
        if_scores = -self.iforest.fit_predict(X_scaled)

        # LOF
        self.lof.fit(X_scaled)
        lof_scores = -self.lof.predict(X_scaled)

        # Autoencoder
        if self.autoencoder is None:
            self.autoencoder = self._build_autoencoder(X_scaled.shape[1])
            self.autoencoder.fit(
                X_scaled,
                X_scaled,
                epochs=20,
                batch_size=32,
                verbose=0
            )

        reconstructions = self.autoencoder.predict(X_scaled, verbose=0)
        reconstruction_error = np.mean(
            np.square(X_scaled - reconstructions), axis=1
        )

        # Normalize scores
        final_score = (
            (if_scores > 0).astype(int)
            + (lof_scores > 0).astype(int)
            + (reconstruction_error > np.percentile(reconstruction_error, 95)).astype(int)
        )

        df_result = df.copy()
       
        # Add baseline statistics for explainability
        for col in ["src_bytes", "dst_bytes", "count", "srv_count"]:
          df_result[f"{col}_mean"] = df[col].mean()

          df_result["anomaly_score"] = final_score
          df_result["is_anomaly"] = df_result["anomaly_score"] >= 2

        return df_result
