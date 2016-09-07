from accounts import views
from accounts.forms import LoginForm
from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^login/', login, {
        'authentication_form': LoginForm,
        'template_name': 'registration/login.html',
    }, name='login'),
    url(r'^logout/', logout_then_login, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^friends/page-(?P<page>\d+)/$', views.friend_list, name='friend_list'),
    url(r'^friend/add/(?P<username>\w+)/$', views.add_friend, name='add_friend'),
    url(r'^friend/remove/(?P<username>\w+)/$', views.remove_friend, name='remove_friend'),
]
