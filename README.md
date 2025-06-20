# TrakNor Backend

Django 4.2 project structured with Clean Architecture. The core layers are:

- **domain** – pure business entities (dataclasses).
- **application** – services with business logic.
- **infrastructure** – Django models and serializers.
- **presentation** – API views and URL routes.

## Setup

```bash
cp .env.example .env
# adjust DEBUG and ALLOWED_HOSTS as needed

# Optional: enable SQLite fallback
# echo "DATABASE_URL=sqlite:///db.sqlite3" >> .env
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # optional
```

Set `ENABLE_2FA=true` in `.env` to activate the optional two-factor flows.

## Running

```bash
python manage.py runserver
```

### User Roles

Users can have one of the following roles:

- `admin`
- `manager`
- `technician` (default)

Use `/api/profile/` to fetch the authenticated user's data including `role`.

## Como gerar docs localmente

```bash
python manage.py spectacular --file schema/openapi.json
spectacular --validate schema/openapi.json
```

## Lint and Test

```bash
ruff check . --select F,E,I
pytest
```

## Build & Quality

[![Coverage](https://img.shields.io/codecov/c/github/ClimaTrak/TrakNor-Backend?label=coverage)](https://codecov.io/gh/ClimaTrak/TrakNor-Backend)
## Quality Gates

Atualmente o `mypy` roda em modo relaxado (`strict` desabilitado) para liberar o pipeline. Consulte a issue `chore/sbXX-enable-mypy-strict` para acompanhar a reativação.


## API Overview

- `/api/auth/` – JWT authentication (login, refresh, register).
- `/api/equipment/` – list and create equipment. Supports CSV import via `/import/` endpoint.
- `/api/work-orders/` – manage work orders and view history.
- `/api/work-orders/{id}/status/` – change work order status with revision check.
- Deleting a work order performs a soft delete.
- `/api/dashboard/summary/` – dashboard metrics.
- `/api/reports/` – generate PDF or Excel equipment/work order reports.

Note: This repository is a Django backend. Node.js/TypeScript features mentioned in some tasks are not applicable.
