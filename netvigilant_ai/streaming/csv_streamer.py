import pandas as pd
import time


class CSVStreamer:
    """
    Simulates real-time CSV streaming by yielding chunks.
    """

    def __init__(self, chunk_size: int = 50, delay: float = 0.5):
        self.chunk_size = chunk_size
        self.delay = delay

    def stream(self, df: pd.DataFrame):
        """
        Generator that yields dataframe chunks.
        """
        total_rows = len(df)

        for start in range(0, total_rows, self.chunk_size):
            end = start + self.chunk_size
            chunk = df.iloc[start:end]
            yield chunk
            time.sleep(self.delay)
