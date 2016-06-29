from django.shortcuts import render
from recruit.models import Post


def index(request):
    posts = Post.objects.all()
    return render(request, 'recruit/index.html', {'posts':posts})

