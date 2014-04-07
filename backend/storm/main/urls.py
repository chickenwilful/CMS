from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns(
    '',
    url(r'^$', views.main_page, name="main.main_page"),
    url(r'^(?P<emergency_situation_id>\d+)$', views.main_page, name='main.main_page_event'),
    url(r'^getPSI$', views.get_psi, name='main.get_psi'),

)
