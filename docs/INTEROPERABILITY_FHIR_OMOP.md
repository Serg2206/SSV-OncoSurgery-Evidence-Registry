# Interoperability Plan: FHIR + OMOP

## Why
Interoperability enables multicenter collaboration, external validation, and scalable evidence generation.

## Strategy
1. Internal canonical schema remains simple and versioned.
2. Add mapping tables to:
- FHIR resources (Patient, Encounter, Condition, Procedure, Observation).
- OMOP CDM concepts for outcomes research compatibility.
3. Maintain code-set governance (SNOMED, ICD, LOINC where applicable).

## Practical Mapping Examples
- `tumor_site` -> FHIR Condition.bodySite / OMOP condition_concept_id.
- `procedure_type` -> FHIR Procedure.code / OMOP procedure_concept_id.
- `complication_clavien_max` -> Observation profile with constrained value set.

## Governance Rules
- Mapping updates require review by clinical + data stewards.
- Mapping version is pinned per report cycle.
- Backward compatibility notes required when mappings change.
