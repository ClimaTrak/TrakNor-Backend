# TrakNor Backend

Django 4.2 project structured with Clean Architecture. The core layers are:

- **domain** – pure business entities (dataclasses).
- **application** – services with business logic.
- **infrastructure** – Django models and serializers.
- **presentation** – API views and URL routes.

## Setup

```bash
cp .env.example .env
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

## Running

```bash
python manage.py runserver
```

## Lint and Test

```bash
ruff check .
pytest
```

## API Overview

- `/api/auth/` – JWT authentication (login, refresh, register).
- `/api/equipment/` – list and create equipment. Supports CSV import via `/import/`.
- `/api/work-orders/` – manage work orders and view history.
- `/api/dashboard/summary/` – dashboard metrics.

Note: This repository is a Django backend. Node.js/TypeScript features mentioned in some tasks are not applicable.
