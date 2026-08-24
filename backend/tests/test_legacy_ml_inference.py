from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_obsolete_ml_pipeline_module_is_not_present() -> None:
    assert not (ROOT / "backend" / "app" / "ml_pipeline.py").exists()


def test_canonical_inference_module_exists() -> None:
    assert (ROOT / "backend" / "app" / "inference.py").is_file()


def test_api_uses_canonical_inference_path() -> None:
    api_source = (ROOT / "backend" / "app" / "api.py").read_text()

    assert "from app.inference import predict_score" in api_source
    assert "ml_pipeline" not in api_source


def test_canonical_inference_uses_artifact_loader() -> None:
    inference_source = (
        ROOT / "backend" / "app" / "inference.py"
    ).read_text()

    assert "from ml.artifact import load_artifact" in inference_source
    assert 'artifact["pipeline"]' in inference_source
