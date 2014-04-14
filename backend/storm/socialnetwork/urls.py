"""socialnetwork urls module
Defines URLs used by the socialnetwork app

@author: Muhammad Fazli Bin Rosli
Matriculation Number: N1302335L
"""
from django.conf.urls import patterns, url
from socialnetwork import views

urlpatterns = patterns(
    'socialnetwork.views',
    url(r'^$', views.social, name="social"),
    url(r'^test$', views.social_test, name="social_test"),
    url(r'^post$', views.social_post, name="social_post"),
    url(r'^(?P<site>\w+)/logout$', views.social_logout, name="social_logout"),
    url(r'^(?P<site>\w+)/auth$', views.social_auth, name="social_auth"),
    url(r'^(?P<site>\w+)/callback$', views.social_callback, name="social_callback"),
    url(r'^(?P<site>\w+)/page$', views.social_page_select, name="social_page_select"),
)
