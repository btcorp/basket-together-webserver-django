# -*- coding:utf-8 -*-

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, View, CreateView

from accounts.forms import LoginForm
from accounts.forms import UserProfileForm, SignupForm
from accounts.models import Friendship, Profile
from basket_together.settings import dev, prod


class SignupView(CreateView):
    model = get_user_model()
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def get_success_url(self):
        next_url = self.request.GET.get('next', '')
        return settings.LOGIN_URL + '?next=' + next_url

    def form_valid(self, form):
        self.object= form.save()
        Profile.objects.create(user=self.object)
        return super(SignupView, self).form_valid(form)


def LoginView(request):
    local_host  = request.META['HTTP_HOST']
    if local_host == '127.0.0.1:8000' or local_host == 'localhost:8000':
        facebook_key = dev.SOCIAL_AUTH_FACEBOOK_KEY
    else:
        facebook_key = prod.SOCIAL_AUTH_FACEBOOK_KEY

    context = {
        'authentication_form': LoginForm,
        'template_name': 'registration/login.html',
        'extra_context': {
            'SOCIAL_AUTH_FACEBOOK_KEY': facebook_key,
        },
    }
    return login(request, **context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserProfileForm
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        print(form.__class__)
        messages.success(self.request, '프로필이 업데이트 되었습니다.')
        return super(ProfileUpdateView, self).form_valid(form)


class FriendListView(LoginRequiredMixin, ListView):
    model = Friendship
    template_name = 'friend_list.html'
    paginate_by = 10
    context_object_name = 'friends'

    def get_queryset(self):
        friends = Friendship.objects.filter(from_friend=self.request.user)
        return [fs.to_friend for fs in friends]


# 친구 추가/삭제에 대한 클래스
class FriendHandlingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next', '')
        if request.is_ajax():                   # ajax 요청 여부 확인
            return HttpResponse(next_url)
        else:
            return HttpResponseRedirect(next_url)

    def post(self, request, *args, **kwargs):
        friend = get_object_or_404(get_user_model(), id=kwargs['id'])
        friend_list = list(i.to_friend.username for i in Friendship.objects.filter(from_friend=friend))
        if request.user not in friend_list:
            Friendship(from_friend=request.user, to_friend=friend).save()
        return self.get(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        friend = get_object_or_404(get_user_model(), id=kwargs['id'])
        friendship = Friendship.objects.filter(from_friend=request.user, to_friend=friend)
        friendship.delete()
        return self.get(request, *args, **kwargs)
