from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean
from typing import Any

from fastapi import FastAPI, HTTPException

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_CSV = ROOT / "patient_outcomes_template.csv"
REPORTS_DIR = ROOT / "reports" / "quarterly"
EVAL_TEMPLATE = ROOT / "analytics" / "eval" / "model_eval_report.template.json"

app = FastAPI(
    title="SSV Evidence Registry API",
    description="Quality, reporting, and evaluation endpoints for oncology evidence registry.",
    version="0.1.0",
)


def _to_bool(raw: str) -> bool:
    return str(raw).strip().lower() in {"true", "1", "yes", "y"}


def _load_rows() -> list[dict[str, str]]:
    if not REGISTRY_CSV.exists():
        raise HTTPException(status_code=404, detail="Registry CSV not found")
    with REGISTRY_CSV.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/quality/summary")
def quality_summary() -> dict[str, Any]:
    rows = _load_rows()
    if not rows:
        raise HTTPException(status_code=400, detail="Registry has no rows")

    los = [float(r["los_days"]) for r in rows if r.get("los_days")]
    complication = [int(r["complication_clavien_max"]) for r in rows if r.get("complication_clavien_max")]

    readmission_count = sum(_to_bool(r.get("readmission_30d", "")) for r in rows)
    reoperation_count = sum(_to_bool(r.get("reoperation_30d", "")) for r in rows)
    mortality_count = sum(_to_bool(r.get("mortality_30d", "")) for r in rows)
    icu_count = sum(_to_bool(r.get("icu_admission", "")) for r in rows)
    severe_complication_count = sum(1 for value in complication if value >= 3)

    by_tumor_site: dict[str, int] = {}
    for row in rows:
        tumor_site = row.get("tumor_site", "unknown")
        by_tumor_site[tumor_site] = by_tumor_site.get(tumor_site, 0) + 1

    total = len(rows)
    return {
        "records_total": total,
        "los_mean_days": round(mean(los), 2) if los else None,
        "complication_clavien_mean": round(mean(complication), 2) if complication else None,
        "readmission_30d_rate": round(readmission_count / total, 4),
        "reoperation_30d_rate": round(reoperation_count / total, 4),
        "mortality_30d_rate": round(mortality_count / total, 4),
        "icu_admission_rate": round(icu_count / total, 4),
        "severe_complication_rate": round(severe_complication_count / total, 4),
        "by_tumor_site": by_tumor_site,
    }


@app.get("/api/v1/reports/quarterly/latest")
def latest_quarterly_report() -> dict[str, Any]:
    if not REPORTS_DIR.exists():
        raise HTTPException(status_code=404, detail="Quarterly reports directory does not exist")

    candidates = sorted(REPORTS_DIR.glob("*.md"))
    if not candidates:
        raise HTTPException(status_code=404, detail="No quarterly reports found")

    latest = candidates[-1]
    return {
        "period": latest.stem,
        "file": str(latest.relative_to(ROOT)).replace("\\", "/"),
        "content": latest.read_text(encoding="utf-8"),
    }


@app.get("/api/v1/reports/quarterly/{period}")
def quarterly_report(period: str) -> dict[str, Any]:
    file_path = REPORTS_DIR / f"{period}.md"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Report not found for period: {period}")

    return {
        "period": period,
        "file": str(file_path.relative_to(ROOT)).replace("\\", "/"),
        "content": file_path.read_text(encoding="utf-8"),
    }


@app.get("/api/v1/eval/template")
def eval_template() -> dict[str, Any]:
    if not EVAL_TEMPLATE.exists():
        raise HTTPException(status_code=404, detail="Model evaluation template not found")

    return json.loads(EVAL_TEMPLATE.read_text(encoding="utf-8"))


@app.get("/api/v1/dashboard/partner-demo")
def partner_demo_dashboard() -> dict[str, Any]:
    """Compact payload for pilot demos and partner presentations."""
    quality = quality_summary()
    latest_report = latest_quarterly_report()

    return {
        "program": "SSV OncoSurgery Evidence Pilot",
        "snapshot": {
            "records_total": quality["records_total"],
            "los_mean_days": quality["los_mean_days"],
            "severe_complication_rate": quality["severe_complication_rate"],
            "readmission_30d_rate": quality["readmission_30d_rate"],
            "mortality_30d_rate": quality["mortality_30d_rate"],
        },
        "reporting": {
            "latest_period": latest_report["period"],
            "latest_report_file": latest_report["file"],
        },
        "commercial": {
            "pilot_duration_weeks": 12,
            "starter_pilot_usd": 9000,
            "pro_pilot_usd": 18000,
            "network_pilot_usd_from": 35000,
        },
        "next_actions": [
            "Expand cohort to 30-50 records",
            "Enable risk-adjusted stratification",
            "Finalize partner pilot kickoff package",
        ],
    }
