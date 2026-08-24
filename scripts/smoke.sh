#!/usr/bin/env bash

set -u

echo "========== SMOKE: PYTHON IMPORT =========="
python -c "import sys; sys.path.insert(0, 'backend'); import app.main; print('Application import OK')"

echo
echo "========== SMOKE: HEALTH ENDPOINT =========="
python - <<'PY'
import sys

sys.path.insert(0, "backend")

from fastapi.testclient import TestClient
from app.main import app

with TestClient(app) as client:
    response = client.get("/health")
    assert response.status_code == 200, response.text
    assert response.json() == {"status": "healthy"}, response.json()

print("Health endpoint OK")
PY

echo
echo "========== SMOKE: COMPLETE =========="
