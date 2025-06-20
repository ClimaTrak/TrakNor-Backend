from django.contrib.auth import get_user_model

User = get_user_model()  # Isso evita carregar o model antes da hora

