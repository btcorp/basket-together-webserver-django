from django.shortcuts import render
from recruit.models import Post
from django.views.generic import ListView


class IndexView(ListView):
    queryset = Post.objects.order_by('-registered_date')[:12]
    template_name = 'recruit/index.html'
    context_object_name = 'posts'
