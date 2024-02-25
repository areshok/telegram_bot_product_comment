import os
import subprocess

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from product.models import Score, Marketplace, Score
from data.files import get_path_to_file

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает Админа, Добавляет оценки, Маркеплейсы'


    def handle(self, *args, **options):
        create_db()
        create_admin()
        create_score()



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