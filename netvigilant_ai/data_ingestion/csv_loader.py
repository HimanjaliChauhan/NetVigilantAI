import pandas as pd

# REQUIRED CSV SCHEMA (LOCKED)
REQUIRED_COLUMNS = [
    "timestamp",
    "protocol",
    "duration",
    "src_bytes",
    "dst_bytes",
    "count",
    "srv_count",
    "source_id"
]


def load_and_validate_csv(csv_path: str) -> pd.DataFrame:
    """
    Loads and validates a summarized network traffic CSV file.
    """

    # Load CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"Failed to load CSV file: {e}")

    # Check required columns
    missing_cols = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Keep only required columns
    df = df[REQUIRED_COLUMNS]

    # Convert timestamp
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    except Exception:
        raise ValueError("Invalid timestamp format")

    # Sort by time
    df = df.sort_values("timestamp").reset_index(drop=True)

    return df


# Test run
if __name__ == "__main__":
    path = "sample_data/sample_traffic.csv"
    data = load_and_validate_csv(path)
    print("CSV loaded successfully")
    print(data)
