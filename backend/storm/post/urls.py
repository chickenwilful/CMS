from django.conf.urls import patterns, url
from post import views

urlpatterns = patterns(
    '',
    url(r'^post_list/$', views.post_list, name='post.post_list'),
    url(r'^post_retrieve/(?P<post_id>\d+)/$', views.post_retrieve, name='post.post_retrieve'),
    url(r'^post_create/$', views.post_create, name='post.post_create'),
    url(r'^post_update/(?P<post_id>\d+)/$', views.post_update, name='post.post_update'),
    url(r'^post_delete/(?P<post_id>\d+)/$', views.post_delete, name='post.post_delete'),
    url(r'^create/$', views.create, name='post.create'),
)
