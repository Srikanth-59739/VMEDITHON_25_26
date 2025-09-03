import json
from pathlib import Path
import pandas as pd
import numpy as np
from utils import ensure_columns, parse_ts, TS_COL
REQUIRED = ['patient_id', 'timestamp']  # example required columns
TS_COL = 'timestamp'

def parse_ts(ts_str):
    # Example timestamp parser, replace with actual logic
    return pd.to_datetime(ts_str, errors='coerce')

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]

    missing_cols = [col for col in REQUIRED if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    df[TS_COL] = df[TS_COL].apply(parse_ts)
    df = df.dropna(subset=[TS_COL]).sort_values(['patient_id', TS_COL])
    return df


def make_supervised(df: pd.DataFrame, horizon_min: int = 60) -> tuple[pd.DataFrame, dict]:
    df = df.copy()
    df = df.sort_values(["patient_id", TS_COL])


# Lags (last 3 readings and doses)
    for k in [1, 2, 3]:
        df[f"glucose_lag{k}"] = df.groupby("patient_id")["glucose_mgdl"].shift(k)
        df[f"dose_lag{k}"] = df.groupby("patient_id")["dosage_units"].shift(k)
        df[f"carbs_lag{k}"] = df.groupby("patient_id")["carbs_g"].shift(k)


# Time features
    df["hour"] = df[TS_COL].dt.hour
    df["dayofweek"] = df[TS_COL].dt.dayofweek


# Target: glucose at t + horizon
    freq_min = np.median(np.diff(df[TS_COL].dropna().astype("int64")).astype(float)) / 1e9 / 60.0
# robust default if timestamps irregular
    steps = max(1, int(round(horizon_min / max(freq_min, 5))))
    df["target_glucose"] = df.groupby("patient_id")["glucose_mgdl"].shift(-steps)


# Drop rows without target or lags
    feature_cols = [
    "glucose_mgdl",
    "dosage_units",
    "carbs_g",
    "glucose_lag1", "glucose_lag2", "glucose_lag3",
    "dose_lag1", "dose_lag2", "dose_lag3",
    "carbs_lag1", "carbs_lag2", "carbs_lag3",
    "hour", "dayofweek",
    ]


    df = df.dropna(subset=feature_cols + ["target_glucose"]) # keep only complete rows
    spec = {"features": feature_cols, "target": "target_glucose", "horizon_min": horizon_min}
    return df[feature_cols + ["patient_id", TS_COL, "target_glucose"]], spec




def save_feature_spec(spec: dict, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)




def load_feature_spec(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)