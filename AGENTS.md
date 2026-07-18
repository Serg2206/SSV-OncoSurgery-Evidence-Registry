# AGENTS.md

Agent operating guide for SSV-OncoSurgery-Evidence-Registry.

## Purpose
Coordinate human experts and AI agents to:
- maintain evidence-grade clinical registry quality,
- generate reproducible analytics,
- prepare publication-ready outputs,
- support ethical, compliant commercialization.

## Core Agent Roles
1. IntakeAgent
- Validates incoming records against schema.
- Flags missing mandatory fields and invalid code sets.

2. QAAgent
- Runs data quality checks (completeness, consistency, range checks).
- Produces weekly quality dashboard artifacts.

3. ProtocolAgent
- Detects protocol drift and pathway deviations.
- Suggests updates for protocol versioning.

4. AnalyticsAgent
- Generates KPI and risk-adjusted outcome tables.
- Produces survival and complication analyses.

5. PublicationAgent
- Builds methods, results tables, and figure drafts.
- Outputs manuscript-ready markdown sections.

6. GovernanceAgent
- Enforces de-identification constraints and access policy checks.
- Blocks unsafe exports.

## Human-in-the-Loop Gates
- Gate 1: Clinical reviewer approval before data freeze.
- Gate 2: PI approval before quarterly report publication.
- Gate 3: Compliance approval before external data sharing.

## Required Outputs Per Cycle
- `analytics/eval/quality_report.json`
- `analytics/eval/model_eval_report.json`
- `reports/quarterly/YYYY-Qx.md`
- `governance/change-log.md` update

## Safety Rules
- Never store direct PHI in repository.
- Never expose record-level data in public reports.
- Always preserve versioned schema and dictionary history.
- All agent outputs must be reproducible from a tagged dataset snapshot.

## Suggested Runtime Stack
- Orchestration: CrewAI or LangGraph.
- Retrieval: LlamaIndex with vector store (Qdrant/pgvector).
- Evaluation/Observability: LangSmith, OpenTelemetry.
- Serving: FastAPI + containerized deployment.
