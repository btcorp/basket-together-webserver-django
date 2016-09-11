from django.conf.urls import url
from recruit import views

urlpatterns = [
    url(r'^post/page-(?P<page>\d+)/$', views.post_list, name='post_list'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^search/$', views.post_search, name='post_search'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post/participation/(?P<pk>\d+)/add/$', views.add_participation, name='add_participation'),
    url(r'^post/participation/(?P<pk>\d+)/remove/$', views.remove_participation, name='remove_participation'),
    url(r'^participations/page-(?P<page>\d+)/$', views.participations, name='participations'),
]