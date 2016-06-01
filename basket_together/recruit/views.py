from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'recruit/post_list.html', {'posts': posts})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('recruit.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'recruit/post_edit.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # comments = get_object_or_404(Comment, post_id=pk)
    return render(request, 'recruit/post_detail.html', {'post': post})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('recruit.views.post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'recruit/post_edit.html', {'form': form})


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('recruit.views.post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('recruit.views.post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'recruit/add_comment_to_post.html', {'form': form})


def post_search(request):
    word = request.POST['word']
    posts = Post.objects.filter(title__contains=word) or Post.objects.filter(content__contains=word)
    return render(request, 'recruit/post_list.html', {'posts': posts})


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('recruit.views.post_detail', pk=post_pk)
