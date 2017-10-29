from django.db import models
from django.urls import reverse

class User(models.Model):
	first_name = models.CharField(max_length=50, help_text="First Name")
	last_name = models.CharField(max_length=50, help_text="Last Name")
	groups = models.ManyToManyField('Group', help_text="Groups this user is associated with")
	events = models.ManyToManyField('Event', help_text="Events created by this user")
	friends = models.ManyToManyField('User', help_text="Friends of this user")
	picture = models.ImageField(upload_to='images/user_pics/', default='images/user_pics/Default.jpg')

	def __str__(self):
		return self.first_name + " " + self.last_name

	def get_absolute_url(self):
		return reverse('user-detail', args=[str(self.id)])

class Event(models.Model):
	eventTitle = models.CharField(max_length=50, help_text="Event Name")
	location = models.CharField(max_length=100, help_text="Location")
	summary = models.TextField(max_length=1000, help_text="Enter a brief description of the Event")
	groups = models.ManyToManyField('Group', help_text="Groups this user is associated with")
	host = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	events = models.ManyToManyField('Event', help_text="Events created by this user")
	invited = models.ManyToManyField('User', help_text="These users are invited to the event", related_name="invited")
	joined = models.ManyToManyField('User', help_text="Thse users have joined the Event", related_name="joined")
	picture = models.ImageField(upload_to='images/')

	def __str__(self):
		return self.eventTitle

	def get_absolute_url(self):
		return self.id

class Group(models.Model):
	name = models.CharField(max_length=200, help_text="Enter a name for the group")
	description = models.TextField(max_length=1000, help_text="Enter a bried description of the group")
	members = models.ManyToManyField(User, help_text="Select members for this group")
	events = models.ManyToManyField(Event, help_text="Add an event to this group")
	images = models.ImageField(upload_to="images/")

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('group-detail', args=[str(self.id)])