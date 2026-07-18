# Release Plan: SSV-OncoSurgery-Evidence-Registry

## Objective
Deliver an evidence-grade registry that can support internal quality governance and external publication workflows.

## R1 (Weeks 1-2): Foundation
- Approve registry charter and governance roles.
- Freeze v1 data dictionary.
- Add de-identification standard and access matrix.
- Commit initial protocol templates.

Done when:
- All mandatory metadata fields are defined.
- Validation rules exist for required fields and type checks.

## R2 (Weeks 3-6): Data Intake and QA
- Import first retrospective cohort (20-50 cases).
- Run missingness and consistency checks.
- Document data quality exceptions and remediation.

Done when:
- Mandatory field completeness >= 95%.
- No critical schema violations remain.

## R3 (Weeks 7-10): Analytics MVP
- Compute core KPIs (LOS, readmission, reoperation, 30d mortality).
- Build risk-adjusted stratification by stage and ASA class.
- Produce first reproducible quarterly report.

Done when:
- Re-running analytics on same snapshot gives identical results.
- Report includes methods, limitations, and bias note.

## R4 (Weeks 11-14): Validation Layer
- Internal calibration review.
- External benchmark template populated.
- Prepare publication-ready table package.

Done when:
- Validation memo approved.
- Publication pipeline checklist completed.

## R5 (Weeks 15-18): Agentization and Platform API
- Add agent configuration baseline and role prompts.
- Implement API contracts for quality reports and analytics jobs.
- Add observability baseline (traces, job logs, report lineage).

Done when:
- Agent pipeline runs end-to-end on a tagged sample snapshot.
- API can return last quality report and last quarterly report metadata.

## R6 (Weeks 19-24): Productization and Monetization Readiness
- Create Starter/Pro/Enterprise packaging definitions.
- Prepare partner pilot playbook and onboarding checklist.
- Publish pricing assumptions and value metric framework.

Done when:
- One pilot-ready deployment profile is documented.
- One partner-facing evidence package template is finalized.

## Ongoing Cadence
- Weekly: QA huddle and issue triage.
- Monthly: protocol drift review and update.
- Quarterly: evidence report release and archive snapshot.

## Go-To-Market Cadence
- Monthly: showcase one measurable clinical insight artifact.
- Quarterly: release one public methods/evidence note.
- Biannual: partner pilot review and commercialization iteration.

## Risk Controls
- Keep raw and curated datasets strictly separated.
- Never store PHI in repository.
- Use immutable snapshot tags for each report cycle.
- Require review before schema changes.
