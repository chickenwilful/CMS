from django.conf.urls import patterns, url
from event import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index),
    url(r'^map/$', views.map),
    url(r'^event_create/$', views.event_create),
    url(r'^event_list/$', views.event_list),
    url(r'^event_retrieve/(?P<event_id>\d+)/$', views.event_retrieve),
)
