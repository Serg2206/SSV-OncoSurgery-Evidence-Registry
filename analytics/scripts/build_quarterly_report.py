from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean


def to_bool(raw: str) -> bool:
    return str(raw).strip().lower() in {"true", "1", "yes", "y"}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_report(rows: list[dict[str, str]], period: str) -> str:
    total = len(rows)
    los = [float(r["los_days"]) for r in rows if r.get("los_days")]
    clavien = [int(r["complication_clavien_max"]) for r in rows if r.get("complication_clavien_max")]

    readmission_count = sum(to_bool(r.get("readmission_30d", "")) for r in rows)
    reoperation_count = sum(to_bool(r.get("reoperation_30d", "")) for r in rows)
    mortality_count = sum(to_bool(r.get("mortality_30d", "")) for r in rows)
    severe_complication_count = sum(1 for value in clavien if value >= 3)

    return f"""# Quarterly Evidence Report ({period})

## Dataset Scope
- Records analyzed: {total}
- Source: de-identified registry template

## Core Outcomes
- Mean length of stay: {mean(los):.2f} days
- Mean max Clavien-Dindo grade: {mean(clavien):.2f}
- 30-day readmission rate: {readmission_count/total:.2%}
- 30-day reoperation rate: {reoperation_count/total:.2%}
- 30-day mortality rate: {mortality_count/total:.2%}
- Severe complications (Clavien >= 3): {severe_complication_count/total:.2%}

## Interpretation
This is a demonstration report generated from sample retrospective records. It validates the reporting pipeline structure and reproducibility workflow.

## Limitations
- Small sample size.
- Demonstration-only dataset.
- Not intended for clinical decision-making.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="patient_outcomes_template.csv")
    parser.add_argument("--period", default="2026-Q3")
    parser.add_argument("--output", default="reports/quarterly/2026-Q3.md")
    args = parser.parse_args()

    rows = load_rows(Path(args.input))
    report = build_report(rows, args.period)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    main()
