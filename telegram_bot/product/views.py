from django.shortcuts import render

# Create your views here.
from .models import CommentProduct

def index(request):
    comments =  CommentProduct.scores.all()
    context = {
        'comments': comments,

    }
    return render(request, 'base.html', context)