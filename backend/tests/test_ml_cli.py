from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "hotel_reservations_sample.csv"
)


def test_ml_module_trains_and_writes_artifact(tmp_path):
    output = tmp_path / "smart_hotel_model.pkl"

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ml",
            "--dataset",
            str(FIXTURE),
            "--output",
            str(output),
        ],
        cwd=Path(__file__).resolve().parents[2],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output.exists()
    assert output.stat().st_size > 0
    assert "Model saved to:" in result.stdout
    assert "roc_auc:" in result.stdout
