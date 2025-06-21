# Architecture Notes

This project follows a Clean Architecture approach with domain, application, infrastructure and presentation layers. API documentation is generated automatically via drf-spectacular.

## Settings Profiles

- `config.settings.dev` – development defaults.
- `config.settings.ci` – used in CI with SQLite fallback.
- `config.settings.prod` – production; requires `DATABASE_URL`.
