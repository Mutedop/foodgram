from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254, unique=True,
        verbose_name='Адрес электронной почты'
    )
    username = models.CharField(
        max_length=150, unique=True, blank=False,
        verbose_name='Уникальный юзернейм'
    )
    first_name = models.CharField(
        max_length=150, blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150, blank=False,
        verbose_name='Фамилия'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Издатель'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='subscription_unique'
        )]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
