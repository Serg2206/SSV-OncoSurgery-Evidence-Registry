from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app


def main() -> None:
    client = TestClient(app)

    checks = [
        ("/ready", ["status", "checks"]),
        ("/api/v2/dashboard/full", ["generated_at", "overall", "trends_by_period", "risk_stratified"]),
        ("/api/public/sales-kpi", ["program", "generated_at", "kpi", "commercial", "compliance_note"]),
    ]

    for endpoint, required_fields in checks:
        response = client.get(endpoint)
        if response.status_code != 200:
            raise AssertionError(f"{endpoint} returned {response.status_code}, expected 200")

        payload = response.json()
        for field in required_fields:
            if field not in payload:
                raise AssertionError(f"{endpoint} missing field '{field}'")

        print(f"OK: {endpoint}")

    print("Smoke tests passed")


if __name__ == "__main__":
    main()
