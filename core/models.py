from typing import List

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS: List[str] = []

    class Meta:
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'
