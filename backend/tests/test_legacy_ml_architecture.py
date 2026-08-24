from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_obsolete_training_pipeline_is_not_present() -> None:
    assert not (ROOT / "backend" / "models" / "train_models.py").exists()


def test_legacy_model_artifacts_are_not_tracked() -> None:
    legacy_artifacts = (
        ROOT / "models" / "best_model.pkl",
        ROOT / "models" / "lightgbm.pkl",
        ROOT / "models" / "randomforest.pkl",
    )

    for artifact in legacy_artifacts:
        assert not artifact.exists()


def test_canonical_training_module_exists() -> None:
    assert (ROOT / "backend" / "ml" / "training.py").is_file()
    assert (ROOT / "backend" / "ml" / "__main__.py").is_file()
