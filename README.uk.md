# SSV-OncoSurgery-Evidence-Registry (UK)

Мова: [English](README.md) | [Русский](README.ru.md)

Платформа доказової аналітики в онкохірургії з підтримкою агентів, автоматизованої звітності та готовністю до комерційних пілотів.

## Що всередині
- FastAPI для якості даних, звітів і dashboard.
- Повний dashboard JSON з трендами по періодах і risk-stratified блоками.
- Docker і production compose профіль з healthcheck/readiness.
- Матеріали для партнерських пілотів і монетизації.

## Швидкий запуск
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Або через Docker:
```bash
docker compose up --build -d
```

## Ключові endpoint
- GET /health
- GET /ready
- GET /api/v1/quality/summary
- GET /api/v1/dashboard/partner-demo
- GET /api/v1/dashboard/full
- GET /api/v1/reports/quarterly/latest

## Документи
- Partner one-pager: docs/PARTNER_PILOT_ONE_PAGER.md
- Pilot landing: docs/PILOT_LANDING.md
- Partner OpenAPI spec: docs/openapi.partner.yaml
