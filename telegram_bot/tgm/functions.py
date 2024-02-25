import math

from django.conf import settings
from django.db.models import Min

from tgm.models import TelegramUser
from product.models import Marketplace, Score, Product, CommentProduct





def marketplace_buttoms() -> list:
    """Функция создает кнопки под количество маркетплейсов"""
    marketplases = Marketplace.objects.all()
    count = len(marketplases)
    count_lists = math.ceil(count / settings.COUNT_BUTTONS_IN_LINE)
    result = []
    names = []

    for marketplase in marketplases:
        names.append(marketplase.name)

    for _ in range(count_lists):
        result.append([])

    list_edit = 0
    for i in range(count):
        if i != 0:
            if i % settings.COUNT_BUTTONS_IN_LINE == 0:
                list_edit += 1
        result[list_edit].append(names[i])
    return result


def score_buttoms() -> list:
    """Фйнкция создает кнопки под оценки"""
    scores = Score.objects.all()
    result = []
    for score in scores:
        result.append([str(score.score)])
    return result


def filter_marketplase() -> str:
    """Функция создает фильтр для маркептлейсов"""

    marketplases = Marketplace.objects.all()
    names = []
    for marketplase in marketplases:
        names.append(marketplase.name)
    return '|'.join(names)


def filter_score() -> str:
    """Функция создает фильтр для оценок"""

    scores = Score.objects.all()
    names = []
    for score in scores:
        names.append(str(score.score))
    return '|'.join(names)


def check_user(t_user):
        """Проверка есть ли пользователь в дб.
        Если нет, то добавляется, если есть, то
        проверяется фактическая информация в дб с тем какие сейчас
        у пользователя данные"""

        if TelegramUser.objects.filter(telegram_id=t_user['id']).exists():
            user = TelegramUser.objects.get(telegram_id=t_user['id'])
            if user.first_name != t_user['first_name']:
                user.first_name = t_user['first_name']
            if user.last_name != t_user['last_name']:
                user.last_name = t_user['last_name']
            if user.username != t_user['username']:
                user.username = t_user['username']

        else:
            TelegramUser.objects.create(
                username=t_user['username'],
                first_name=t_user['first_name'],
                telegram_id=t_user['id']
            )

def check_product(article):
    """Проверка есть по данному артикулу товар в дб"""

    return Product.objects.filter(id=article).exists()


def get_mid_score():
    """Возвращает среднне число оценки"""

    number = Score.objects.filter(mid_score=True)
    if len(number) == 0:
        all_scores = Score.objects.all()
        mid = len(all_scores) // 2
        mid_score = all_scores[mid]
    else:
        mid_score = number[0]
    return mid_score

def get_min_score():
    """Возвращает минимальное число оценки"""

    min = Score.objects.aggregate(Min('score'))
    return min['score__min']


def check_comment(product, user):
    return CommentProduct.objects.filter(
        product=product,
        user_telegram=user,
    ).exists()
        


