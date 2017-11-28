from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),

	# create
	url(r'^g/new$', views.GroupCreate.as_view(), name='create_group'),
	url(r'^e/new$', views.create_event, name='create_event'),

	# view
	url(r'^u/(?P<id>\d+)$', views.view_user, name='user'),
	url(r'^g/(?P<id>\d+)$', views.view_group, name='group'),
	url(r'^e/(?P<id>\d+)$', views.view_event, name='event'),

	# edit
	url(r'^settings/$', views.settings, name='settings'),
	url(r'^g/(?P<id>\d+)/edit$', views.GroupEdit.as_view(), name='edit_group'),
	url(r'^e/(?P<id>\d+)/edit$', views.edit_event, name='edit_event'),

	# interact
	url(r'^u/(?P<id>\d+)/(?P<action>\w+)$', views.user_action, name='user_action'),
	url(r'^g/(?P<id>\d+)/(?P<action>\w+)$', views.group_action, name='group_action'),
	url(r'^e/(?P<id>\d+)/(?P<action>\w+)$', views.event_action, name='event_action'),
	url(r'^search/$', views.search, name='search'),
]
