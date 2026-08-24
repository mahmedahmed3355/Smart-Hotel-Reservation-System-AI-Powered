from pathlib import Path


def test_env_example_uses_canonical_model_artifact():
    env_path = Path(__file__).resolve().parents[2] / ".env.example"
    env_source = env_path.read_text()

    assert "MODEL_PATH=models/smart_hotel_model.pkl" in env_source
    assert "MODEL_PATH=models/best_model.pkl" not in env_source
