from django.conf.urls import patterns, url
from socialnetwork import views

urlpatterns = patterns(
    '',
    url(r'^$', views.social_login, name="socialnetwork.social_login"),
    url(r'^post$', views.social_post, name="socialnetwork.social_post"),
    url(r'^(?P<site>\w+)/logout$', views.social_logout, name="socialnetwork.social_logout"),
    url(r'^facebook$', views.facebook_page_select, name="socialnetwork.facebook_page_select"),
    url(r'^facebook_process$', views.facebook_process, name="socialnetwork.facebook_process"),
)
