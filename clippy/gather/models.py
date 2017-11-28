from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True, help_text="Friends of this user")
    picture = models.ImageField(upload_to='images/user/', default='images/user/placeholder.png')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_absolute_url(self):
        return reverse('user', args=[str(self.id)])

class EventGroup(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a name for the group")
    description = models.TextField(max_length=1000, blank=True, null=True, help_text="Enter a brief description of the group")
    members = models.ManyToManyField(Profile, related_name="groups", help_text="Select members for this group")
    picture = models.ImageField(upload_to="images/group/", blank=True, null=True)

    class Meta: 
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group', args=[str(self.id)])

class Event(models.Model):
    title = models.CharField(max_length=50, help_text="Event Name")
    location = models.CharField(max_length=100, help_text="Location")
    time = models.DateTimeField(help_text="Enter a time for the event")
    description = models.TextField(max_length=1000, blank=True, null=True, help_text="Enter a brief description of the Event")
    hosts = models.ManyToManyField(Profile, related_name="hosting", help_text="These users are hosting the Event")
    groups = models.ManyToManyField(EventGroup, blank=True, related_name="events", help_text="Groups this user is associated with")
    invited = models.ManyToManyField(Profile, blank=True, related_name="invited", help_text="These users are invited to the event")
    joined = models.ManyToManyField(Profile, blank=True, related_name="joined", help_text="These users have joined the Event")
    hidden = models.ManyToManyField(Profile, blank=True, related_name="hidden", help_text="These users have hidden the Event")
    picture = models.ImageField(upload_to='images/event/', blank=True, null=True)

    class Meta: 
        ordering = ["time"]

    def __str__(self):
        return self.title
