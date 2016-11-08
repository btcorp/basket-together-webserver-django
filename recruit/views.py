# -*- coding:utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from recruit.forms import CommentForm, PostForm
from recruit.models import Participation, Comment, Post


class PostListView(ListView):
    queryset = Post.objects.order_by('-registered_date')
    template_name = 'recruit/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        return context


class PostCreateView(CreateView):
    model = Post
    template_name = 'recruit/post_new.html'
    form_class = PostForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostCreateView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        add_participation(self.request, self.object.id)
        messages.success(self.request, '포스팅이 등록되었습니다.')
        return HttpResponseRedirect(self.get_success_url())


class PostDetailView(DetailView):
    model = Post
    template_name = 'recruit/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        post = self.get_object()

        if user.id:
            is_friend = True if user.from_friends.filter(to_friend=post.author) else False
        else:
            is_friend = None
        participation = Participation.objects.filter(post=post)
        attend_users = ''
        for user in post.attend_users():
            attend_users += user + ', '

        context['isFriend'] = is_friend
        context['participation'] = participation
        context['attend_users'] = attend_users[:-2]
        return context


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'recruit/post_new.html'


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('recruit:post_list')


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'recruit/add_comment_to_post.html'
    form_class = CommentForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CommentCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = post
        return super(CommentCreateView, self).form_valid(form)


def post_search(request):
    word = request.POST['word']
    posts = Post.objects.filter(
        Q(title__icontains=word) |
        Q(content__icontains=word) |
        Q(author__username__icontains=word)
    )
    return render(request, 'recruit/post_list.html', {'posts': posts})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('recruit:post_detail', pk=post_pk)


@login_required
def add_participation(request, pk):
    post = get_object_or_404(Post, pk=pk)
    next_url = request.GET.get('next', '')
    Participation.objects.create(post=post, user=request.user)
    post.attend_count += 1
    post.save()
    return HttpResponseRedirect(next_url)


@login_required
def remove_participation(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bookmark = get_object_or_404(Participation, post=post, user=request.user)
    bookmark.delete()
    post.attend_count -= 1
    post.save()
    return redirect('recruit:post_detail', pk=pk)


class ParticipationListView(ListView):

    template_name = 'recruit/participation_list.html'
    context_object_name = 'participations'
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ParticipationListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Participation.objects.filter(user=self.request.user)
