from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TelegramUserViewSet, get_qrcode


router = SimpleRouter()

router.register(r'tgm', TelegramUserViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('product/<id>/download_qrcode', get_qrcode, name='qrcode')

]


