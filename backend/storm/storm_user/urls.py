from django.conf.urls import patterns, url
from storm_user import views

urlpatterns = patterns(
    '',
    url(r'^user_login/$', views.user_login, name='user.user_login'),
    url(r'^user_logout/$', views.user_logout, name='user.user_logout'),
    url(r'^user_add/$', views.user_add, name='user.user_add'),
    url(r'^user_detail/(?P<user_id>\d+)/$', views.user_detail, name='user.user_detail'),
    url(r'^user_edit/(?P<user_id>\d+)/$', views.user_edit, name='user.user_edit'),
    url(r'^login/$', views.login, name='user.login'),
)
