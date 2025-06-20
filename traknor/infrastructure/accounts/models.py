from django.db import models

from traknor.infrastructure.models.user import User  # noqa: F401


class AccountProfile(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
