from django.conf.urls import url

from chat import views

urlpatterns = [
    url(r'^message/save/$', views.message_save, name='message_save'),
    url(r'^messages/$', views.get_messages, name='messages'),
]