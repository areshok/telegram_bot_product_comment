import math

from django.db import models
from django.db.models.query import QuerySet
from django.apps import apps




class CommentManager(models.Manager):
    """Менеджер показывает только коментарии
    с оценками от средней оценки до низкой."""

    def get_mid(self):
        """Функция выдает среднее число из таблицы оценка"""

        model = apps.get_model(app_label='product', model_name='Score')
        number = model.objects.filter(mid_score=True)
        if len(number) == 0:
            all_scores = model.objects.all()
            mid = len(all_scores) // 2
            mid_score = all_scores[mid]
        else:
            mid_score = number[0]
        return mid_score
    
    def get_queryset(self) -> QuerySet:
        """Возвращает коментарии в которых оценка ниже или равна заданной"""

        model = apps.get_model(app_label='product', model_name='Score')
        return super().get_queryset().filter(user_score__lte=self.get_mid())
