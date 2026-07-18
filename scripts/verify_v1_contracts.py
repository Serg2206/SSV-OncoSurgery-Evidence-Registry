from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import sys

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app

CONTRACTS_DIR = ROOT / "contracts" / "v1"


def _is_type(value: Any, expected: str) -> bool:
    if expected == "int":
        return isinstance(value, int)
    if expected == "float":
        return isinstance(value, float)
    if expected == "str":
        return isinstance(value, str)
    if expected == "dict":
        return isinstance(value, dict)
    if expected == "list":
        return isinstance(value, list)
    if expected == "number_or_null":
        return value is None or isinstance(value, (int, float))
    return False


def _assert_fields(payload: dict[str, Any], required_fields: dict[str, str], context: str) -> None:
    for key, expected_type in required_fields.items():
        if key not in payload:
            raise AssertionError(f"Missing field '{key}' in {context}")
        if not _is_type(payload[key], expected_type):
            raise AssertionError(
                f"Field '{key}' in {context} has wrong type. "
                f"Expected {expected_type}, got {type(payload[key]).__name__}"
            )


def verify_contract(client: TestClient, contract_path: Path) -> None:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    endpoint = contract["endpoint"]

    response = client.get(endpoint)
    if response.status_code != 200:
        raise AssertionError(f"{endpoint} returned {response.status_code}, expected 200")

    payload = response.json()
    _assert_fields(payload, contract["required_fields"], endpoint)

    required_headers = contract.get("required_headers", {})
    for header_key, expected_value in required_headers.items():
        actual = response.headers.get(header_key)
        if actual != expected_value:
            raise AssertionError(
                f"Header '{header_key}' mismatch for {endpoint}: expected '{expected_value}', got '{actual}'"
            )

    if "snapshot_required_fields" in contract:
        snapshot = payload.get("snapshot")
        if not isinstance(snapshot, dict):
            raise AssertionError(f"Field 'snapshot' in {endpoint} must be dict")
        _assert_fields(snapshot, contract["snapshot_required_fields"], f"{endpoint}.snapshot")

    if "overall_required_fields" in contract:
        overall = payload.get("overall")
        if not isinstance(overall, dict):
            raise AssertionError(f"Field 'overall' in {endpoint} must be dict")
        _assert_fields(overall, contract["overall_required_fields"], f"{endpoint}.overall")


def main() -> None:
    client = TestClient(app)
    contracts = sorted(CONTRACTS_DIR.glob("*.contract.json"))
    if not contracts:
        raise SystemExit("No v1 contracts found")

    for contract_path in contracts:
        verify_contract(client, contract_path)
        print(f"OK: {contract_path.name}")

    print("All v1 contracts validated successfully")


if __name__ == "__main__":
    main()
