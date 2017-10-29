from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^u/(?P<id>\d+)$', views.user, name='user'),
	url(r'^g/(?P<id>\d+)$', views.group, name='group'),
]