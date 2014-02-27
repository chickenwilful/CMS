from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^event/', include('event.urls')),
    url(r'^main/', include('main.urls')),
    url(r'^post/', include('post.urls')),
    url(r'^user/', include('storm_user.urls')),
)
