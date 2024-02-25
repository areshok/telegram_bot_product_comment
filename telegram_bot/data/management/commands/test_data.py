import os
import csv
import subprocess
import random

from dotenv import load_dotenv
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Min, Max

from data.files import get_path_to_file
from product.models import Score, Marketplace, Product, ProductMarketplace, Score,CommentProduct
from tgm.models import TelegramUser

load_dotenv()
User = get_user_model()


class Command(BaseCommand):
    help = """Делает то же что и data, с дополнительными тевтовыми данными"""

    def handle(self, *args, **options):
        create_db()
        create_admin()
        create_score()
        create_marketplase()
        create_t_user()
        create_product()
        create_product_marketplase()
        create_comment()


def create_db():
    """Функция делает миграцию"""

    subprocess.call(['python', 'manage.py', 'makemigrations'])
    subprocess.call(['python', 'manage.py', 'migrate'])

def create_admin():
    """Создает суперпользователя"""

    user = User.objects.create_user(
        username=os.getenv('ADMIN_LOGIN'),
        email=os.getenv('ADMIN_EMAIL'),
        password=os.getenv('ADMIN_PASSWORD'),)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print('УЗ admin создан')

def create_score():
    """Добавляет в дб оценки"""

    file = get_path_to_file(__name__, 'score')
    with open(file, mode='r', encoding='utf-8') as f:
        Score.objects.all().delete()
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            Score.objects.create(**line)
    print('Оценки созданы')

def create_marketplase():
    """Добавляет в бд маркетплейсы"""

    file = get_path_to_file(__name__, 'marketplase')
    with open(file, mode='r', encoding='utf-8') as f:
        Marketplace.objects.all().delete()
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            Marketplace.objects.create(**line)
    print('Маркетплейсы созданы')

def create_t_user():
    """Добавляет тестовых пользоватлей телеграм"""

    file = get_path_to_file(__name__, 't_user')
    with open(file, mode='r', encoding='utf-8') as f:
        TelegramUser.objects.all().delete()
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            TelegramUser.objects.create(**line)
    print('Тестовые телеграм пользователи созданы')

def create_product():
    """Добавляет в дб тестовые товары"""

    file = get_path_to_file(__name__, 'product')
    with open(file, mode='r', encoding='utf-8') as f:
        Product.objects.all().delete()
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            Product.objects.create(**line)
    print('Тестовые товары созданы')


def create_product_marketplase():
    """Добавляет в дб тестовые ссылки на товар"""

    products = Product.objects.all()
    marketplases = Marketplace.objects.all()
    for product in products:
        for marketpalse in marketplases:
            ProductMarketplace.objects.create(
                product=product,
                marketplace=marketpalse,
                url=f'https://{marketpalse.name}/{product.name}'
            )
    print('Тестовые ссылки на товары созданы')

def create_comment():
    """Добавляет в дб тестовые комментарии"""

    products = Product.objects.all()
    t_users = TelegramUser.objects.all()
    score_min = Score.objects.aggregate(Min('score'))
    score_max = Score.objects.aggregate(Max('score'))
    for product in products:
        for _ in range(100):
            for t_user in t_users:
                user_score = random.randint(
                    score_min['score__min'], score_max['score__max']
                )
                score = Score.objects.get(score=user_score)
                CommentProduct.objects.create(
                    product=product,
                    user_telegram=t_user,
                    user_score=score,
                    comment='test'
                )
    print('Тествоые коментарии готовы')
