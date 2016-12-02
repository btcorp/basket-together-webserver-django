from django.shortcuts import render
from recruit.models import Post


def index(request):
    posts = Post.objects.order_by('-registered_date')[:12]
    return render(request, 'recruit/index.html', {'posts': posts})

