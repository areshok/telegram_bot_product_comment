import os
import mimetypes

from django.shortcuts import render
from rest_framework import viewsets

from wsgiref.util import FileWrapper

from django.http import FileResponse


from django.http import HttpResponse, Http404


from django.conf import settings

from .serializers import UserSerializer, TelegramUserSerializer

from product.models import Product
from user.models import User
from tgm.models import TelegramUser

class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



def get_qrcode(request, id):
    """Скачивание QRCODE."""

    product = Product.objects.get(id=id)
    full_path = os.path.join(settings.MEDIA_ROOT, str(product.qrcode))
    with open(full_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(full_path)}'
            return response
    raise Http404






