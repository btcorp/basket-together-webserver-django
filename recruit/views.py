# -*- coding:utf-8 -*-

from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import BaseCreateView

from recruit.forms import CommentForm, PostForm
from recruit.models import Participation, Comment, Post


class PostListView(ListView):
    queryset = Post.objects.order_by('-registered_date')
    template_name = 'recruit/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        region = self.request.GET.get('region')
        if region:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.filter(address1__icontains=region)
                return queryset
        return super(PostListView, self).get_queryset()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'recruit/post_new.html'
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        add_participation(self.request, self.object.id)
        messages.success(self.request, '포스팅이 등록되었습니다.')
        return HttpResponseRedirect(self.get_success_url())


class PostDetailView(DetailView, BaseCreateView):
    model = Post
    template_name = 'recruit/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        post = self.get_object()

        if user.id:
            is_friend = True if user.from_friends.filter(to_friend=post.author) else False
        else:
            is_friend = None
        participation = Participation.objects.filter(post=post)
        attend_user_str = ''
        for user in post.attend_users():
            attend_user_str += user + ', '

        context['isFriend'] = is_friend
        context['participation'] = participation
        context['attend_user_str'] = attend_user_str[:-2]
        context['attend_users'] = post.attend_users()
        context['form'] = self.get_form_class()
        return context

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = post
        return super(BaseCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        return super(BaseCreateView, self).post(request, *args, **kwargs)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'recruit/post_new.html'


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('recruit:post_list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

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
        Q(author__username__icontains=word) |
        Q(address1__icontains=word) |
        Q(address2__icontains=word)
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


class ParticipationListView(LoginRequiredMixin, ListView):

    template_name = 'recruit/participation_list.html'
    context_object_name = 'participations'
    paginate_by = 10

    def get_queryset(self):
        return Participation.objects.filter(user=self.request.user)
