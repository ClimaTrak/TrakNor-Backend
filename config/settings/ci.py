from .base import *  # noqa: F401,F403,F405

DATABASES = {
    "default": env.db(  # noqa: F405
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'tmp' / 'ci_db.sqlite3'}",  # noqa: F405
    )
}

SECRET_KEY = "ci-secret-key"
ALLOWED_HOSTS = ["*"]

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
