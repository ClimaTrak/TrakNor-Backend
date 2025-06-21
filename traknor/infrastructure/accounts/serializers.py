from rest_framework import serializers

from .models import AccountProfile


class AccountProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountProfile
        fields = ["id", "name"]
