# Deployment Paths

## 1. Local Research Mode
- Run validation and analytics scripts against local de-identified CSV snapshots.
- Recommended for protocol iteration and methods development.

## 2. Docker Compose Team Mode
- Service A: API (FastAPI)
- Service B: worker queue for long-running analytics
- Service C: PostgreSQL (+ optional pgvector)
- Service D: observability collector

## 3. Cloud Production Mode
- Kubernetes deployment with managed Postgres.
- Object storage for snapshot archives.
- OIDC/SSO for role-based access.
- WAF and audit logging enabled.

## Baseline SLOs
- Data quality report generation: < 15 min per batch.
- Quarterly full report pipeline: < 2 hours.
- API availability target: >= 99.5%.

## Release Discipline
- Tag each validated snapshot.
- Semantic versioning for schema and pipeline.
- Changelog entry for every governance-impacting change.
