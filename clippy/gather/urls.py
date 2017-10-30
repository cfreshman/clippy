from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^u/(?P<id>\d+)$', views.user, name='user'),
	url(r'^g/(?P<id>\d+)$', views.group, name='group'),
	url(r'^event/$', views.event, name='event'),
	url(r'^manager/$', views.manager, name='manager'),
	url(r'^settings/$', views.settings, name='settings'),
]