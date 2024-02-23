from django.contrib import admin

# Register your models here.
from .models import TelegramUser

admin.site.register(TelegramUser)