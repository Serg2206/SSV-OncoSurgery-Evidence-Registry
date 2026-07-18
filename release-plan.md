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

## Ongoing Cadence
- Weekly: QA huddle and issue triage.
- Monthly: protocol drift review and update.
- Quarterly: evidence report release and archive snapshot.

## Risk Controls
- Keep raw and curated datasets strictly separated.
- Never store PHI in repository.
- Use immutable snapshot tags for each report cycle.
- Require review before schema changes.
