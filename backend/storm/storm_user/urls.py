from django.conf.urls import patterns, url
from storm_user import views

urlpatterns = patterns(
    '',
    url(r'^user_changepassword/(?P<user_id>\d+)/$', views.user_changepassword, name='user.user_changepassword'),
    url(r'^user_list/$', views.user_list, name='user.user_list'),
    url(r'^user_login/$', views.user_login, name='user.user_login'),
    url(r'^user_logout/$', views.user_logout, name='user.user_logout'),
    url(r'^user_create/$', views.user_create, name='user.user_create'),
    url(r'^user_retrieve/(?P<user_id>\d+)/$', views.user_retrieve, name='user.user_retrieve'),
    url(r'^user_update/(?P<user_id>\d+)/$', views.user_update, name='user.user_update'),
    url(r'^login/$', views.login, name='user.login'),
    url(r'^user_delete/(?P<user_id>\d+)/$', views.user_delete, name='user.user_delete'),
)
