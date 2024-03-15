from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings

from .models import CommentProduct, Score


def index(request):
    return render(request, 'index.html',)

def comments(request):
    comments_list =  CommentProduct.scores.all()
    paginator = Paginator(comments_list, settings.ELEMENT_IN_PAGE)
    page_number = request.GET.get('page', 1)
    comments = paginator.page(page_number)
    context = {
        'page_obj': comments,
    }
    return render(request, 'product/comment.html', context)

def comment_detail(request, id):
    comment = CommentProduct.objects.get(id=id)
    context = {
        'comment': comment
    }
    return render(request, 'product/comment_detail.html', context)

def scores(request):
    scores = Score.objects.all()
    context = {
        'page_obj': scores
    }
    return render(request,)


