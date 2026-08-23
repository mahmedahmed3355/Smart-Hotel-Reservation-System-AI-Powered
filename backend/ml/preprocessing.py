from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

from ml.schema import CATEGORICAL_FEATURES, NUMERIC_FEATURES


def build_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OrdinalEncoder(
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, list(NUMERIC_FEATURES)),
            ("categorical", categorical_pipeline, list(CATEGORICAL_FEATURES)),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def validate_features(frame: pd.DataFrame) -> None:
    missing = [column for column in NUMERIC_FEATURES + CATEGORICAL_FEATURES if column not in frame.columns]

    if missing:
        raise ValueError(
            f"Missing required features: {missing}"
        )


def prepare_features(frame: pd.DataFrame) -> pd.DataFrame:
    validate_features(frame)

    columns = list(NUMERIC_FEATURES + CATEGORICAL_FEATURES)

    return frame.loc[:, columns].copy()
