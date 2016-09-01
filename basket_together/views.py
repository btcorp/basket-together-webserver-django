from django.shortcuts import render
from recruit.models import Post


def index(request):
    posts = Post.objects.order_by('-meeting_date')[:8]
    return render(request, 'recruit/index.html', {'posts': posts})

