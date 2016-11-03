from django.conf.urls import url
from recruit import views

urlpatterns = [
    url(r'^posts/$', views.PostListView.as_view(), name='post_list'),
    url(r'^post/new/$', views.PostCreateView.as_view(), name='post_new'),
    url(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.CommentCreateView.as_view(), name='add_comment_to_post'),
    url(r'^search/$', views.post_search, name='post_search'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post/participation/(?P<pk>\d+)/add/$', views.add_participation, name='add_participation'),
    url(r'^post/participation/(?P<pk>\d+)/remove/$', views.remove_participation, name='remove_participation'),
    url(r'^participations/$', views.ParticipationListView.as_view(), name='participation_list'),
]
