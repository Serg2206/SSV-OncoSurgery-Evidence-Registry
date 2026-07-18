# API Versioning and Deprecation Policy

## Current State
- Active version: `v2`
- Legacy version: `v1` (deprecated)

## Deprecation Mechanics
- `v1` endpoints return deprecation headers:
  - `Deprecation: true`
  - `Sunset: 2027-01-31`
  - `Link: </api/v2/meta/versioning>; rel="successor-version"`

## Migration Guidance
1. New integrations must use `v2`.
2. Existing `v1` clients should migrate as soon as possible.
3. `v1` receives critical fixes only.

## Discovery Endpoint
- `GET /api/v2/meta/versioning`

## Public Sales Endpoint
For public partner pages and teaser integrations, use aggregate-only payload:
- `GET /api/public/sales-kpi`

No row-level data is exposed by this endpoint.
