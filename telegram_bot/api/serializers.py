from rest_framework import serializers

from user.models import User
from tgm.models import TelegramUser


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для пользователей"""

    class Meta:
        model = User
        fields = ['id', 'username']


class PasswordSerializer(serializers.Serializer):
    """Сериалайзер для пароля пользователя.
    Для смены пароля пользователя
    """

    pass

class TelegramUserSerializer(serializers.ModelSerializer):
    """Сериалайзер телеграм пользователей"""

    class Meta:
        model = TelegramUser
        fields = ['id', 'username', 'telegram_id',]