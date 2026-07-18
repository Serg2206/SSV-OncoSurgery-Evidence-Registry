# SSV-OncoSurgery-Evidence-Registry (RU)

Язык: [English](README.md) | [Українська](README.uk.md)

Платформа доказательной аналитики в онкохирургии с поддержкой агентов, автоматизированной отчетности и готовностью к коммерческим пилотам.

## Что внутри
- API на FastAPI для качества данных, отчетов и dashboard.
- Полный dashboard JSON с трендами по периодам и risk-stratified блоками.
- Docker и production compose профиль с healthcheck/readiness.
- Материалы для партнерских пилотов и монетизации.

## Быстрый запуск
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Или через Docker:
```bash
docker compose up --build -d
```

## Ключевые endpoint
- GET /health
- GET /ready
- GET /api/v1/quality/summary
- GET /api/v1/dashboard/partner-demo
- GET /api/v1/dashboard/full
- GET /api/v1/reports/quarterly/latest

## Документы
- Partner one-pager: docs/PARTNER_PILOT_ONE_PAGER.md
- Pilot landing: docs/PILOT_LANDING.md
- Partner OpenAPI spec: docs/openapi.partner.yaml
