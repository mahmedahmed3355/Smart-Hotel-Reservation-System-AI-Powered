import os
import subprocess
import sys
from pathlib import Path


def test_ml_module_trains_and_writes_artifact(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]
    dataset = repo_root / "backend/tests/fixtures/hotel_reservations_sample.csv"
    output = tmp_path / "smart_hotel_model.pkl"

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "backend")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ml",
            "--dataset",
            str(dataset),
            "--output",
            str(output),
        ],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output.is_file()
    assert output.stat().st_size > 0
    assert "Model saved to:" in result.stdout
    assert "roc_auc:" in result.stdout
