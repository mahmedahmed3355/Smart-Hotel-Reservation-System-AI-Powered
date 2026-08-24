import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"

if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def load_ml_pipeline(mock_model):
    sys.modules.pop("app.ml_pipeline", None)

    with (
        patch("builtins.open", mock_open(read_data=b"model")),
        patch("pickle.load", return_value=mock_model),
    ):
        return importlib.import_module("app.ml_pipeline")


def test_predict_booking_returns_first_prediction():
    mock_model = MagicMock()
    mock_model.predict.return_value = [1]

    ml_pipeline = load_ml_pipeline(mock_model)

    result = ml_pipeline.predict_booking(
        {
            "lead_time": 10,
            "arrival_date_week_number": 20,
        }
    )

    assert result == 1
    mock_model.predict.assert_called_once()


def test_predict_booking_passes_features_as_dataframe():
    mock_model = MagicMock()
    mock_model.predict.return_value = [0]

    ml_pipeline = load_ml_pipeline(mock_model)

    features = {
        "lead_time": 15,
        "arrival_date_week_number": 30,
    }

    result = ml_pipeline.predict_booking(features)

    assert result == 0

    dataframe = mock_model.predict.call_args.args[0]

    assert dataframe.shape == (1, 2)
    assert dataframe.iloc[0]["lead_time"] == 15
    assert dataframe.iloc[0]["arrival_date_week_number"] == 30
