"""Settings for continuous integration environments."""

from __future__ import annotations

import os

# Provide fallbacks so CI runs without additional configuration.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "ci-secret-key")

from .base import *  # noqa: E402,F403

DEBUG = False

# Use an in-memory database for faster test execution.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Speed up password hashing and disable real email sending during tests.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

