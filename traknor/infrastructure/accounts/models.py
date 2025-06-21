from django.db import models


class AccountProfile(models.Model):
    name: str = models.CharField(max_length=255)  # type: ignore[assignment]

    def __str__(self) -> str:
        return self.name
