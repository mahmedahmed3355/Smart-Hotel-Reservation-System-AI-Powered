from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_dependency_metadata_is_consistent():
    result = subprocess.run(
        [sys.executable, "scripts/check_dependency_metadata.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Dependency metadata is consistent" in result.stdout
