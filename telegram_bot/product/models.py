from django.db import models


import uuid



from django.db import models

from django.dispatch import receiver

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.conf import settings

import qrcode
from io import BytesIO



from .managers import CommentManager

from tgm.models import TelegramUser




class Marketplace(models.Model):
    """ Таблица маркеплейсов"""

    name = models.CharField(
        max_length=30
    )

    class Meta:
        verbose_name = 'Маркетплейс'
        verbose_name_plural = 'Маркетплейсы'

    def __str__(self):
        return self.name

class Product(models.Model):
    """Таблица товаров"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=30
    )
    qrcode = models.ImageField(
        upload_to='qrcode',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

@receiver(models.signals.post_save, sender=Product)
def generate_qrcode(sender, instance, created, *args, **kwargs):
    """Создает qrcode и сохраняет его в оперативной памяти
    после сохраняет на сервер.
    Функция отрабатывает при создании файла"""

    if created:
        print(instance)
        url = settings.T_BOT_URL + str(instance.id)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer)
        filename = f'{instance.name}_{instance.id}.png'
        filebuffer = InMemoryUploadedFile(
            buffer,
            None,
            filename,
            'image/png',
            None,
            None,
        )
        instance.qrcode.save(filename, filebuffer)
        instance.save()


class ProductMarketplace(models.Model):
    """Таблица ссылок товара на маркетплейсах."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    marketplace = models.ForeignKey(
        Marketplace,
        on_delete=models.CASCADE
    )
    url = models.TextField()

class Score(models.Model):
    score = models.PositiveIntegerField(
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    mid_score = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['score',]
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'{self.score}'

class CommentProduct(models.Model):
    """
    Таблица с коментариями пользователей о товареы
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    user_telegram = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE
    )
    user_score =  models.ForeignKey(
        Score,
        on_delete=models.SET_NULL,
        null=True,
    )
    comment = models.TextField(
        null=True,
        blank=True
    )

    status = models.BooleanField(
        default=False
    )
    date_create = models.DateTimeField(
        auto_now=True
    )
    objects = models.Manager()  # Стандартный менеджер
    scores = CommentManager()  # Менеджер фильтрует данные по оценкам от 1 до 3

    class Meta:
        ordering = ['-date_create']

    def __str__(self):
        return f'{self.user_telegram} - {self.product} - {self.user_score}'













