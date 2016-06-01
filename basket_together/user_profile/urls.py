from django.conf.urls import url

urlpatterns = [
    url(r'^profile/$', 'user_profile.views.user_profile', name='user_profile'),
]
