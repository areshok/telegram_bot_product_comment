from django.db import models

class TelegramUser(models.Model):
    username = models.CharField(
        max_length=32,
        null=False,
        unique=True
    )
    first_name = models.CharField(
        max_length=64,
        null=False
    )
    last_name = models.CharField(
        max_length=64,
        null=False
    )
    telegram_id = models.PositiveBigIntegerField(
        null=False,
        unique=True
    )

    def __str__(self):
        return f'{self.telegram_id} - {self.username}'
