from django.conf.urls import patterns, url
from socialnetwork import views

urlpatterns = patterns(
    'socialnetwork.views',
    url(r'^$', views.social, name="social"),
    url(r'^post$', views.social_post, name="social_post"),
    url(r'^(?P<site>\w+)/logout$', views.social_logout, name="social_logout"),
    url(r'^facebook/page$', views.facebook_page_select, name="facebook_page_select"),
    url(r'^facebook/process$', views.facebook_process, name="facebook_process"),
    url(r'^twitter/auth$', views.twitter_auth, name="twitter_auth"),
    url(r'^twitter/callback$', views.twitter_callback, name="twitter_callback"),
    url(r'^gplus/auth$', views.gplus_auth, name="gplus_auth"),
    url(r'^gplus/callback$', views.gplus_callback, name="gplus_callback"),
)
