from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from recruit.models import Bookmark, Comment, Post
from recruit.forms import BookmarkForm, CommentForm, PostForm


def post_list(request, page=1):
    try:
        posts = Post.objects.order_by('-registered_date')
        paginator = Paginator(posts, 5)
        page_range = paginator.page_range
        contacts = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    except ObjectDoesNotExist:
        contacts = None
        page_range = 1

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
    try:
        bookmark = Bookmark.objects.filter(user=request.user, post=post)
    except ObjectDoesNotExist:
        bookmark = None
    return render(request, 'recruit/post_detail.html', {'post': post, 'bookmark': bookmark})


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
    posts = Post.objects.filter(title__icontains=word) or Post.objects.filter(content__icontains=word)
    return render(request, 'recruit/post_list.html', {'posts': posts})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('recruit:post_detail', pk=post_pk)


@login_required
def bookmark_save(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.post = post
            bookmark.save()
            next_url = request.GET.get('next', '')
            return HttpResponseRedirect(next_url)
            # return redirect('recruit:bookmark_save' + '?next=' + next_url)
    else:
        form = BookmarkForm()
    return render(request, 'recruit/bookmark_save.html', {'form': form})


@login_required
def bookmark_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bookmark = get_object_or_404(Bookmark, post=post, user=request.user)
    bookmark.delete()
    return redirect('recruit:post_detail', pk=pk)


@login_required
def bookmarks(request, page=1):
    try:
        bookmarks = Bookmark.objects.filter(user=request.user)
        paginator = Paginator(bookmarks, 20)
        page_range = paginator.page_range
        contacts = paginator.page(page)
    except ObjectDoesNotExist:
        contacts = None
        page_range = 1

    return render(request, 'recruit/bookmark_list.html', {'bookmarks': contacts, 'page_range': page_range})