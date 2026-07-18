# SSV-OncoSurgery-Evidence-Registry

Language: English | [Русский](README.ru.md) | [Українська](README.uk.md)

Evidence-grade, agent-ready platform for surgical oncology outcomes, protocol intelligence, and reproducible research products.

## Vision
Build a globally interoperable real-world evidence system that combines:
- clinical rigor,
- agentic automation,
- modern AI workflows,
- publication and commercialization readiness.

## Why this repository
Most medical repositories stop at static datasets or ad-hoc analyses. This project is designed as a full lifecycle system:
1. Capture de-identified clinical outcomes.
2. Validate quality automatically.
3. Run reproducible analytics and model evaluation.
4. Generate publication-ready outputs.
5. Productize insights for education, quality improvement, and B2B services.

## Core Principles
- Privacy by design (de-identification first).
- Reproducibility (same snapshot -> same report).
- Clinical relevance (decision-grade metrics).
- Interoperability (FHIR/OMOP mapping path).
- Governance (clear approvals, audit trail, model-risk controls).

## Current Structure

```text
SSV-OncoSurgery-Evidence-Registry/
  README.md
  AGENTS.md
  data_dictionary_template.csv
  patient_outcomes_template.csv
  release-plan.md

  .github/
    workflows/
      ci.yml

  docs/
    TOP_REPO_INSIGHTS.md
    ARCHITECTURE_AGENTIC.md
    DEPLOYMENT.md
    MONETIZATION.md
    INTEROPERABILITY_FHIR_OMOP.md

  agentflow/
    configs/
      agents.example.yaml
    prompts/
      publication_system_prompt.md

  analytics/
    scripts/
      build_quarterly_report.py
    eval/
      model_eval_report.template.json

  app/
    main.py

  Dockerfile
  docker-compose.yml
  docker-compose.prod.yml

  reports/
    quarterly/
      2026-Q3.md

  governance/
    deidentification-standard.md
```

## Agentic Workflow
Pipeline:
- IntakeAgent -> QAAgent -> ProtocolAgent -> AnalyticsAgent -> PublicationAgent -> GovernanceAgent

Human gates:
- clinical reviewer,
- principal investigator,
- compliance reviewer.

See `AGENTS.md` and `agentflow/configs/agents.example.yaml`.

## AI and Modern Technology Stack (Recommended)
- Orchestration: CrewAI or LangGraph.
- Retrieval/knowledge: LlamaIndex + Qdrant or pgvector.
- API layer: FastAPI.
- Observability: OpenTelemetry.
- Deployment: Docker Compose -> Kubernetes.
- CI guardrails: GitHub Actions schema/data checks.

## Interoperability Strategy
This repository keeps a canonical internal schema and maps outward to:
- HL7 FHIR resources,
- OMOP CDM concepts.

See `docs/INTEROPERABILITY_FHIR_OMOP.md`.

## Product and Monetization Directions
1. Clinical analytics subscription for centers/hospitals.
2. Research collaboration and publication services.
3. Education/certification tracks on evidence and AI workflows.
4. Benchmark data products for approved partners.
5. Implementation consulting for registry deployment.

See `docs/MONETIZATION.md`.

## API Surface
Implemented FastAPI service in `app/main.py` with endpoints:
- `GET /health`
- `GET /ready`
- `GET /api/v1/*` (deprecated, migration headers enabled)
- `GET /api/v2/meta/versioning`
- `GET /api/v2/quality/summary`
- `GET /api/v2/reports/quarterly/latest`
- `GET /api/v2/dashboard/partner-demo`
- `GET /api/v2/dashboard/full`
- `GET /api/public/sales-kpi` (aggregate-only public payload)

Run locally:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Quarterly Demo Report
First demo artifact generated and committed:
- `reports/quarterly/2026-Q3.md`

Scripted generator:
- `analytics/scripts/build_quarterly_report.py`

Example command:

```bash
python analytics/scripts/build_quarterly_report.py --period 2026-Q3 --output reports/quarterly/2026-Q3.md
```

## Partner Pilot Pack
Partner-facing one-pager with pilot scope, pricing, and SLA draft:
- `docs/PARTNER_PILOT_ONE_PAGER.md`

Short pilot landing document:
- `docs/PILOT_LANDING.md`

## Containerized Deployment
Run the API with Docker Compose:

```bash
docker compose up --build -d
```

API base URL:
- `http://localhost:8000`

Minimal production profile:

```bash
docker compose -f docker-compose.prod.yml up -d
```

## Partner API Spec
Swagger-oriented partner API examples for sales and pilots:
- `docs/openapi.partner.yaml`

Generated from FastAPI source via:
- `scripts/export_openapi.py`

CI regenerates and validates this file to prevent drift.

## API Versioning Policy
Versioning and deprecation details are documented in:
- `docs/API_VERSIONING.md`

## Gold Metrics
- Mandatory field completeness >= 95%.
- Follow-up capture >= 80% at target interval.
- Complication coding agreement >= 90%.
- Quarterly report turnaround <= 5 days after close.

## Immediate Next Steps
1. Add first 20-50 retrospective de-identified records.
2. Freeze `v1` schema and mapping assumptions.
3. Add risk-adjusted analysis endpoint and dashboard UI.
4. Launch first partner pilot using one-pager scope and SLA model.
