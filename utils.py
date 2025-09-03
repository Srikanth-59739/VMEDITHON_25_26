from datetime import datetime, timezone
import pandas as pd


TS_COL = "timestamp"




def parse_ts(x) -> pd.Timestamp:
    return pd.to_datetime(x, utc=True, errors="coerce").tz_convert(None)




def ensure_columns(df: pd.DataFrame, cols: list[str]):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df




def now_utc_naive():
    return datetime.now(timezone.utc).replace(tzinfo=None)