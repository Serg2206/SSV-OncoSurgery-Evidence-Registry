# Agentic + AI Architecture

## Reference Architecture

1. Data Layer
- `patient_outcomes_template.csv` and future curated snapshots.
- Versioned schema and dictionary as source of truth.

2. Interoperability Layer
- Mapping between internal fields and FHIR/OMOP entities.
- Controlled vocabulary normalization.

3. Agent Orchestration Layer
- IntakeAgent -> QAAgent -> ProtocolAgent -> AnalyticsAgent -> PublicationAgent -> GovernanceAgent.
- Human approvals at predefined gates.

4. Intelligence Layer
- Optional LLM calls for summarization and drafting.
- Statistical scripts for deterministic metrics and risk adjustment.

5. Product Layer
- API endpoints for quality dashboards and report generation.
- Internal portal or partner-facing evidence products.

## Non-Functional Requirements
- Reproducibility: deterministic pipeline where possible.
- Auditability: every report tied to snapshot hash/tag.
- Security: no PHI, least-privilege access.
- Scalability: batch pipeline + async jobs + queue.

## Suggested Tech Stack
- Python: FastAPI, pandas, pydantic.
- Agent framework: CrewAI or LangGraph.
- Retrieval/indexing: LlamaIndex + Qdrant/pgvector.
- Observability: OpenTelemetry.
- Infra: Docker Compose for local, Kubernetes for scale.
