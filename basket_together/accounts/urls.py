from django.conf.urls import url
from django.views.generic import TemplateView
from accounts import views
from accounts.forms import LoginForm

urlpatterns = [
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^accounts/login/', 'django.contrib.auth.views.login',{
        'authentication_form': LoginForm,
    }, name='login'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup_ok/$', TemplateView.as_view(template_name='registration/signup_ok.html'), name='signup_ok'),
]
