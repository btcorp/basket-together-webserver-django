from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm, UserForm
from accounts.forms import SignupForm


@login_required
def user_profile(request):
    """
    Form to update User profile
    """
    if request.method == 'POST':
        userForm = UserForm(request.POST, instance=request.user)
        profileForm = UserProfileForm(request.POST, instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            return render(request, 'loggedin.html')
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
            return HttpResponseRedirect(reverse("accounts:signup_ok"))

    # form = UserCreationForm()
    form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


