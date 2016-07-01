from accounts import views
from accounts.forms import LoginForm
from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^login/', login, {
        'authentication_form': LoginForm,
    }, name='login'),
    url(r'^logout/', logout_then_login, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
]
