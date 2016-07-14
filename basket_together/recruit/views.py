from django.shortcuts import render, get_object_or_404, redirect
from recruit.models import Post, Comment
from recruit.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request, page=1):
    posts = Post.objects.order_by('-registered_date')
    paginator = Paginator(posts, 5)
    page_range = paginator.page_range

    try:
        contacts = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'recruit/post_list.html', {'posts': contacts, 'page_range': page_range})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '포스팅이 등록되었습니다.')
            return redirect('recruit:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'recruit/post_new.html', {'form': form})


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
        return redirect('recruit:post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'recruit/post_new.html', {'form': form})


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('recruit:post_list')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('recruit:post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'recruit/add_comment_to_post.html', {'form': form})


def post_search(request):
    word = request.POST['word']
    posts = Post.objects.filter(title__contains=word) or Post.objects.filter(content__contains=word)
    return render(request, 'recruit/post_list.html', {'posts': posts})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('recruit:post_detail', pk=post_pk)
