from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="docs/openapi.partner.yaml")
    args = parser.parse_args()

    spec = app.openapi()
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # JSON is a valid subset of YAML, so this remains compatible with YAML tooling.
    out_path.write_text(json.dumps(spec, indent=2, ensure_ascii=True), encoding="utf-8")
    print(f"OpenAPI spec exported to {out_path}")


if __name__ == "__main__":
    main()
