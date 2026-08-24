# predictor.py
import pickle

import pandas as pd

from config.settings import MODEL_PATH

# تحميل النموذج مرة واحدة
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def predict_booking(features: dict):
    """
    features: dict من بيانات المستخدم
    """
    df = pd.DataFrame([features])
    prediction = model.predict(df)
    return prediction[0]  # 0/1 أو حسب نموذجك
