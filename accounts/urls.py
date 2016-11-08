from accounts import views
from accounts.forms import LoginForm
from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    url(r'^profile/$', views.ProfileUpdateView.as_view(), name='profile'),
    url(r'^login/', login, {
        'authentication_form': LoginForm,
        'template_name': 'registration/login.html',
    }, name='login'),
    url(r'^logout/', logout_then_login, name='logout'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^friends/$', views.FriendListView.as_view(), name='friend_list'),
    url(r'^friend/add/(?P<id>\d+)/$', views.FriendHandlingView.as_view(), name='add_friend'),
    url(r'^friend/remove/(?P<id>\d+)/$', views.FriendHandlingView.as_view(), name='remove_friend'),
]
