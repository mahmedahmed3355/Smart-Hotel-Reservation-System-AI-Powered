# ml/train_models.py
import os, pickle, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb

DATA_CSV = os.getenv("DATA_CSV", "data/Hotel Reservations.csv")
OUT_DIR = os.getenv("MODEL_DIR", "models")
os.makedirs(OUT_DIR, exist_ok=True)

def load_data(path):
    df = pd.read_csv(path)
    # تنظيف/تكويد بسيط (عدّل حسب EDA بتاعك)
    y = (df["booking_status"] == "Not_Canceled").astype(int)
    X = df.drop(columns=["booking_status", "Booking_ID"], errors="ignore")
    # حوّل الـ categoricals
    for c in X.select_dtypes(include="object").columns:
        X[c] = X[c].astype("category").cat.codes
    X = X.fillna(-1)
    return X, y

def main():
    X, y = load_data(DATA_CSV)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # RandomForest
    rf = RandomForestClassifier(n_estimators=300, max_depth=None, random_state=42, n_jobs=-1)
    rf.fit(Xtr, ytr)
    rf_auc = roc_auc_score(yte, rf.predict_proba(Xte)[:,1])

    # LightGBM
    lgbm = lgb.LGBMClassifier(
        n_estimators=600, learning_rate=0.05, num_leaves=31, subsample=0.9, colsample_bytree=0.9, random_state=42
    )
    lgbm.fit(Xtr, ytr)
    lgb_auc = roc_auc_score(yte, lgbm.predict_proba(Xte)[:,1])

    best, name = (lgbm, "lightgbm.pkl") if lgb_auc >= rf_auc else (rf, "randomforest.pkl")

    with open(os.path.join(OUT_DIR, "randomforest.pkl"), "wb") as f: pickle.dump(rf, f)
    with open(os.path.join(OUT_DIR, "lightgbm.pkl"), "wb") as f: pickle.dump(lgbm, f)
    with open(os.path.join(OUT_DIR, "best_model.pkl"), "wb") as f: pickle.dump(best, f)

    print({"rf_auc": rf_auc, "lgb_auc": lgb_auc, "best": name})

if __name__ == "__main__":
    main()
