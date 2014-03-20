from django.conf.urls import patterns, url
from event import views

urlpatterns = patterns(
    '',
    url(r'^map/$', views.map),
    url(r'^event_list/$', views.event_list, name="event.event_list"),
    url(r'^event_list/(?P<emergency_situation_id>\d+)$', views.event_list, name="event.event_list"),
    url(r'^event_retrieve/(?P<event_id>\d+)/$', views.event_retrieve, name="event.event_retrieve"),
    url(r'^event_create/$', views.event_create, name="event.event_create"),
    url(r'^event_update/(?P<event_id>\d+)/$', views.event_update, name="event.event_update"),
    url(r'^event_delete/(?P<event_id>\d+)/$', views.event_delete, name="event.event_delete"),
)
