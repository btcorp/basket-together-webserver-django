from accounts.forms import UserProfileForm, UserForm
from accounts.forms import SignupForm
from accounts.models import Friendship
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect


@login_required
def user_profile(request):
    """
    Form to update User profile
    """
    if request.method == 'POST':
        userForm = UserForm(request.POST, instance=request.user)
        profileForm = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, '{} 님의 정보가 업데이트되었습니다.'.format(request.user))
            return redirect('index')
    else:
        userForm = UserForm(instance=request.user)
        profileForm = UserProfileForm(instance=request.user.profile)

    args = {}
    # args.update(csrf(request))
    args['userForm'] = userForm
    args['profileForm'] = profileForm
    return render(request, 'profile.html', args)
    # return render_to_response('profile.html', args)


def signup(request):
    """
    Form to register User
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = request.GET.get('next', '')
            return redirect(settings.LOGIN_URL + '?next=' + next_url)

    # form = UserCreationForm()
    form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def friend_list(request, page=1):
    friends = list(i.to_friend for i in request.user.from_friends.all())
    paginator = Paginator(friends, 10)
    contacts = paginator.page(page)
    page_range = paginator.page_range

    return render(request, 'friend_list.html', {'friends': contacts, 'page_range': page_range})


def add_friend(request, username):
    friend = get_object_or_404(get_user_model(), username=username)
    next_url = request.GET.get('next', '')
    friend_list = list(i.to_friend.username for i in Friendship.objects.filter(from_friend=friend))

    if request.user not in friend_list:
        Friendship(from_friend=request.user, to_friend=friend).save()

    return HttpResponseRedirect(next_url)


def remove_friend(request, username):
    next_url = request.GET.get('next', '')
    friend = get_object_or_404(get_user_model(), username=username)
    friendship = Friendship.objects.filter(from_friend=request.user, to_friend=friend)
    friendship.delete()

    return HttpResponseRedirect(next_url)
