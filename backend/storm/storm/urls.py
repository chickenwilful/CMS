from django.conf.urls import patterns, include, url

from django.contrib import admin
import main

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^event/', include('event.urls')),
    url(r'^main/', include('main.urls')),
    url(r'^post/', include('post.urls')),
    url(r'^user/', include('storm_user.urls')),
    url(r'^social/', include('socialnetwork.urls')),
    url(r'^about/', main.views.aboutus, name="main.aboutus"),
    url(r'^contact/', main.views.contactus, name="main.contactus"),
)
