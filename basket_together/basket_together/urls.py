from django.conf.urls import url, include
from django.contrib import admin
from basket_together import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'', include('accounts.urls', namespace='accounts')),
    url(r'^recruit/', include('recruit.urls', namespace='recruit')),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
]
