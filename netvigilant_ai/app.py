import sys
from pathlib import Path

# --------------------------------------------------
# FIX: Add project root to Python path
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# --------------------------------------------------
# Imports
# --------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from netvigilant_ai.data_ingestion.csv_loader import load_and_validate_csv
from netvigilant_ai.ml.anomaly_engine import AnomalyDetectionEngine
from netvigilant_ai.explainability.explainer import AnomalyExplainer
from netvigilant_ai.storyline.timeline_builder import AttackTimelineBuilder
from netvigilant_ai.streaming.csv_streamer import CSVStreamer
from netvigilant_ai.decision.decision_engine import DecisionEngine
from netvigilant_ai.feedback.feedback_manager import FeedbackManager

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="NetVigilant AI", layout="wide")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("NetVigilant AI")
st.sidebar.markdown("Explainable Network Anomaly Detection")

streaming_mode = st.sidebar.checkbox("Enable Streaming Mode")

# --------------------------------------------------
# Main Header
# --------------------------------------------------
st.title("NetVigilant AI Dashboard")
st.caption("Explainable, Near-Real-Time Network Anomaly Detection")

# --------------------------------------------------
# File Upload
# --------------------------------------------------
uploaded_file = st.file_uploader("Upload Network Traffic CSV", type=["csv"])

# --------------------------------------------------
# Initialize Core Engines
# --------------------------------------------------
engine = AnomalyDetectionEngine()
explainer = AnomalyExplainer()
timeline_builder = AttackTimelineBuilder()
decision_engine = DecisionEngine()
feedback_manager = FeedbackManager()

# --------------------------------------------------
# Processing Logic
# --------------------------------------------------
if uploaded_file is not None:
    try:
        df = load_and_validate_csv(uploaded_file)
        st.success("CSV loaded and validated successfully")

        # ---------------- STREAMING / BATCH ----------------
        if streaming_mode:
            st.subheader("Live Stream Processing")
            streamer = CSVStreamer(chunk_size=50, delay=0.5)
            placeholder = st.empty()
            all_results = []

            for chunk in streamer.stream(df):
                chunk_result = engine.run(chunk)
                all_results.append(chunk_result)
                results = pd.concat(all_results)
                placeholder.dataframe(results.tail(50), use_container_width=True)
        else:
            results = engine.run(df)

        # --------------------------------------------------
        # SUMMARY METRICS
        # --------------------------------------------------
        st.subheader("Summary Metrics")
        c1, c2, c3 = st.columns(3)

        c1.metric("Total Sessions", len(results))
        c2.metric("Anomalies Detected", int(results["is_anomaly"].sum()))
        c3.metric("Unique Sources", results["source_id"].nunique())

        # --------------------------------------------------
        # VISUAL ANALYTICS (IMPORTANT FIX)
        # --------------------------------------------------
        st.subheader("Anomaly Visual Analysis")

        results["timestamp"] = pd.to_datetime(results["timestamp"])

        # Trend (SECOND-level, not minute)
        trend_df = results.groupby(
            results["timestamp"].dt.floor("S")
        )["is_anomaly"].sum().reset_index()

        fig_trend = px.line(
            trend_df,
            x="timestamp",
            y="is_anomaly",
            title="Anomaly Trend Over Time",
            labels={"is_anomaly": "Number of Anomalies"}
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # --------------------------------------------------
         # Scatter Plot: Session-level Anomaly Visualization
#         --------------------------------------------------
        st.subheader("Session Anomaly Scatter Plot")

        # Create total traffic feature for visualization
        results["total_bytes"] = results["src_bytes"] + results["dst_bytes"]
        # Convert anomaly flag to color
        results["anomaly_color"] = results["is_anomaly"].apply(
            lambda x: "Anomaly" if x else "Normal"
            )
        fig = px.scatter(
            results,
            x="duration",
            y="total_bytes",
            color="anomaly_color",
            color_discrete_map={
                "Normal": "green",
                "Anomaly": "red"
                },
                hover_data=["protocol", "source_id", "count", "srv_count"],
                title="Scatter Plot of Network Sessions (Red = Anomaly, Green = Normal)"
                )
        st.plotly_chart(fig, use_container_width=True)

        # --------------------------------------------------
        # ALERT TABLE
        # --------------------------------------------------
        st.subheader("Detected Alerts")
        st.dataframe(results, use_container_width=True)

        # --------------------------------------------------
        # Download Anomaly Detection Report
        #  --------------------------------------------------
        st.subheader("Download Analysis Report")
        @st.cache_data
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode("utf-8")
        report_csv = convert_df_to_csv(results)
        st.download_button(
        label="📥 Download Anomaly Detection Report (CSV)",
        data=report_csv,
        file_name="netvigilant_anomaly_report.csv",
        mime="text/csv"
        )

        # --------------------------------------------------
        # EXPLANATION PANEL (MODULE 5)
        # --------------------------------------------------
        st.subheader("Explanation Panel")

        anomalies = results[results["is_anomaly"] == 1]

        if not anomalies.empty:
            idx = st.selectbox(
                "Select anomalous session",
                anomalies.index
            )
            row = anomalies.loc[idx]
            explanation = explainer.explain_row(row)
            st.info(explanation)
        else:
            st.info("No anomalies detected.")

        # --------------------------------------------------
        # ATTACK TIMELINE (MODULE 6)
        # --------------------------------------------------
        st.subheader("Attack Timeline")

        timelines = timeline_builder.build_timelines(results)

        if timelines:
            src = st.selectbox(
                "Select source",
                list(timelines.keys())
            )
            timeline_df = pd.DataFrame(timelines[src])
            st.table(timeline_df)
        else:
            st.info("No attack timelines available.")


        # --------------------------------------------------
        # DECISION SIMULATION & FEEDBACK (MODULE 8)
        # --------------------------------------------------
        st.subheader("Decision Simulation & Feedback Loop")

        if not anomalies.empty:
            didx = st.selectbox(
                "Select alert",
                anomalies.index,
                key="decision"
            )
            selected = anomalies.loc[didx]

            action = st.radio(
                "Choose response",
                ["Ignore", "Monitor", "Quarantine"]
            )

            if st.button("Apply Decision"):
                outcome = decision_engine.simulate_decision(selected, action)
                st.success("Decision simulated")
                st.json(outcome)

            feedback = st.radio(
                "Analyst Feedback",
                ["True Positive", "False Positive"]
            )

            if st.button("Submit Feedback"):
                feedback_manager.record_feedback(selected, feedback)
                st.success("Feedback saved")
                st.info(
                    f"False Positive Rate: {feedback_manager.get_false_positive_rate():.2%}"
                )
        else:
            st.info("No anomalies available for decision simulation.")

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Please upload a CSV file to begin analysis.")
