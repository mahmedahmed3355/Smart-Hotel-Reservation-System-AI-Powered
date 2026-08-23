from __future__ import annotations

from typing import Any

import pandas as pd
from ml.artifact import load_artifact
from ml.preprocessing import prepare_features


def predict_score(payload: dict[str, Any]) -> float:
    frame = pd.DataFrame([payload])
    features = prepare_features(frame)

    artifact = load_artifact()
    pipeline = artifact["pipeline"]

    probability = float(
        pipeline.predict_proba(features)[:, 1][0]
    )

    if not 0.0 <= probability <= 1.0:
        raise ValueError(
            f"Model returned invalid probability: {probability}"
        )

    return probability
