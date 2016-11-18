from django.conf.urls import url
from django.contrib.auth.views import logout_then_login

from accounts import views

urlpatterns = [
    url(r'^profile/$', views.ProfileUpdateView.as_view(), name='profile'),
    url(r'^login/', views.LoginView, name='login'),
    url(r'^logout/', logout_then_login, name='logout'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^friends/$', views.FriendListView.as_view(), name='friend_list'),
    url(r'^friend/add/(?P<id>\d+)/$', views.FriendHandlingView.as_view(), name='add_friend'),
    url(r'^friend/remove/(?P<id>\d+)/$', views.FriendHandlingView.as_view(), name='remove_friend'),
]
