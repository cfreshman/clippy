from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),

	# create
	url(r'^g/new$', views.create_group, name='create_group'),
	url(r'^e/new$', views.create_event, name='create_event'),

	# view
	url(r'^u/(?P<id>\d+)$', views.view_user, name='user'),
	url(r'^g/(?P<id>\d+)$', views.view_group, name='group'),
	url(r'^e/(?P<id>\d+)$', views.view_event, name='event'),

	# edit
	url(r'^settings/$', views.settings, name='settings'),
	url(r'^g/(?P<id>\d+)/edit$', views.edit_group, name='edit_group'),
	url(r'^e/(?P<id>\d+)/edit$', views.edit_event, name='edit_event'),

	# interact
	url(r'^g/(?P<id>\d+)/leave$', views.edit_group, name='leave_group'),
	url(r'^e/(?P<id>\d+)/(?P<reply>\w+)$', views.event_reply, name='event_reply'),
]