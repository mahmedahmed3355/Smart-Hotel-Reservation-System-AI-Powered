# app/inference.py
import os, pickle, numpy as np
import pandas as pd

MODEL_PATH = os.getenv("MODEL_PATH", "models/best_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

NUMERIC_COLS = [
    "no_of_adults","no_of_children", "arrival_year","arrival_month","arrival_date",
    "avg_price_per_room"
]
CAT_COLS = ["market_segment_type","room_type_reserved"]

def preprocess(payload: dict):
    df = pd.DataFrame([payload])
    for c in CAT_COLS:
        if c in df.columns:
            df[c] = df[c].astype("category").cat.codes
        else:
            df[c] = -1
    for c in NUMERIC_COLS:
        df[c] = pd.to_numeric(df.get(c, -1), errors="coerce").fillna(-1)
    return df[NUMERIC_COLS + CAT_COLS]

def predict_score(payload: dict) -> float:
    X = preprocess(payload)
    proba = model.predict_proba(X)[:,1]
    return float(proba[0])
