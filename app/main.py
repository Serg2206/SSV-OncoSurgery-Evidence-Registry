from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
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
    description=(
        "Quality, reporting, dashboard, and partner-facing endpoints "
        "for oncology evidence registry."
    ),
    version="0.2.0",
)


FULL_DASHBOARD_EXAMPLE = {
    "generated_at": "2026-07-18T18:00:00Z",
    "overall": {
        "records_total": 3,
        "los_mean_days": 9.33,
        "severe_complication_rate": 0.3333,
        "readmission_30d_rate": 0.3333,
        "mortality_30d_rate": 0.0,
    },
    "trends_by_period": [
        {
            "period": "2026-Q1",
            "records": 3,
            "los_mean_days": 9.33,
            "severe_complication_rate": 0.3333,
            "readmission_30d_rate": 0.3333,
            "mortality_30d_rate": 0.0,
        }
    ],
    "risk_stratified": {
        "by_stage": {
            "II": {
                "records": 1,
                "mortality_30d_rate": 0.0,
                "severe_complication_rate": 0.0,
            },
            "III": {
                "records": 2,
                "mortality_30d_rate": 0.0,
                "severe_complication_rate": 0.5,
            },
        },
        "by_asa_class": {
            "2": {
                "records": 1,
                "mortality_30d_rate": 0.0,
                "severe_complication_rate": 0.0,
            },
            "3": {
                "records": 1,
                "mortality_30d_rate": 0.0,
                "severe_complication_rate": 0.0,
            },
            "4": {
                "records": 1,
                "mortality_30d_rate": 0.0,
                "severe_complication_rate": 1.0,
            },
        },
    },
}


def _to_bool(raw: str) -> bool:
    return str(raw).strip().lower() in {"true", "1", "yes", "y"}


def _rate(num: int, den: int) -> float:
    if den == 0:
        return 0.0
    return round(num / den, 4)


def _extract_period_from_tag(tag: str) -> str | None:
    # Accept patterns like gastric_q1_2026, q2-2026, cohortQ3_2026.
    match = re.search(r"q([1-4])[_-]?(\d{4})", tag, flags=re.IGNORECASE)
    if not match:
        return None
    quarter, year = match.group(1), match.group(2)
    return f"{year}-Q{quarter}"


def _extract_period(row: dict[str, str]) -> str:
    tag = row.get("study_cohort_tag", "")
    tag_period = _extract_period_from_tag(tag)
    if tag_period:
        return tag_period

    encounter_date = row.get("encounter_date", "")
    try:
        dt = datetime.strptime(encounter_date, "%Y-%m-%d")
        quarter = ((dt.month - 1) // 3) + 1
        return f"{dt.year}-Q{quarter}"
    except ValueError:
        return "unknown"


def _period_sort_key(period: str) -> tuple[int, int]:
    match = re.match(r"^(\d{4})-Q([1-4])$", period)
    if not match:
        return (0, 0)
    return (int(match.group(1)), int(match.group(2)))


def _load_rows() -> list[dict[str, str]]:
    if not REGISTRY_CSV.exists():
        raise HTTPException(status_code=404, detail="Registry CSV not found")
    with REGISTRY_CSV.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _build_metrics(rows: list[dict[str, str]]) -> dict[str, Any]:
    total = len(rows)
    if total == 0:
        return {
            "records": 0,
            "los_mean_days": None,
            "severe_complication_rate": 0.0,
            "readmission_30d_rate": 0.0,
            "mortality_30d_rate": 0.0,
        }

    los = [float(r["los_days"]) for r in rows if r.get("los_days")]
    complication = [int(r["complication_clavien_max"]) for r in rows if r.get("complication_clavien_max")]

    readmission_count = sum(_to_bool(r.get("readmission_30d", "")) for r in rows)
    mortality_count = sum(_to_bool(r.get("mortality_30d", "")) for r in rows)
    severe_complication_count = sum(1 for value in complication if value >= 3)

    return {
        "records": total,
        "los_mean_days": round(mean(los), 2) if los else None,
        "severe_complication_rate": _rate(severe_complication_count, total),
        "readmission_30d_rate": _rate(readmission_count, total),
        "mortality_30d_rate": _rate(mortality_count, total),
    }


def _build_trends(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        period = _extract_period(row)
        grouped.setdefault(period, []).append(row)

    trends: list[dict[str, Any]] = []
    for period in sorted(grouped.keys(), key=_period_sort_key):
        block = _build_metrics(grouped[period])
        trends.append({"period": period, **block})
    return trends


def _build_risk_stratified(rows: list[dict[str, str]], field_name: str) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        bucket = row.get(field_name, "unknown") or "unknown"
        grouped.setdefault(bucket, []).append(row)

    result: dict[str, dict[str, Any]] = {}
    for bucket, bucket_rows in grouped.items():
        metrics = _build_metrics(bucket_rows)
        result[bucket] = {
            "records": metrics["records"],
            "los_mean_days": metrics["los_mean_days"],
            "severe_complication_rate": metrics["severe_complication_rate"],
            "readmission_30d_rate": metrics["readmission_30d_rate"],
            "mortality_30d_rate": metrics["mortality_30d_rate"],
        }
    return result


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, Any]:
    checks = {
        "registry_csv": REGISTRY_CSV.exists(),
        "eval_template": EVAL_TEMPLATE.exists(),
        "reports_dir": REPORTS_DIR.exists(),
    }
    is_ready = all(checks.values())
    if not is_ready:
        raise HTTPException(status_code=503, detail={"status": "not_ready", "checks": checks})
    return {"status": "ready", "checks": checks}


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


@app.get(
    "/api/v1/dashboard/full",
    responses={
        200: {
            "description": "Full dashboard payload for partner pilots and sales demos.",
            "content": {"application/json": {"example": FULL_DASHBOARD_EXAMPLE}},
        }
    },
)
def full_dashboard() -> dict[str, Any]:
    rows = _load_rows()
    if not rows:
        raise HTTPException(status_code=400, detail="Registry has no rows")

    overall_metrics = _build_metrics(rows)
    trends = _build_trends(rows)
    risk_stratified = {
        "by_stage": _build_risk_stratified(rows, "clinical_stage"),
        "by_asa_class": _build_risk_stratified(rows, "asa_class"),
        "by_tumor_site": _build_risk_stratified(rows, "tumor_site"),
    }

    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "overall": {
            "records_total": overall_metrics["records"],
            "los_mean_days": overall_metrics["los_mean_days"],
            "severe_complication_rate": overall_metrics["severe_complication_rate"],
            "readmission_30d_rate": overall_metrics["readmission_30d_rate"],
            "mortality_30d_rate": overall_metrics["mortality_30d_rate"],
        },
        "trends_by_period": trends,
        "risk_stratified": risk_stratified,
    }
