from django.db import models
from django.urls import reverse


# Create your models here.
class User(models.Model):
    first_name = models.CharField (max_length=50, help_text="First Name")
    last_name = models.CharField (max_length=50, help_text="Last Name")
    groups = models.ManyToManyField ('Group', help_text="Groups this user is associated with")
    events = models.ManyToManyField ('Event', help_text="Events created by this user")
    friends = models.ManyToManyField ('User', help_text="Friends of this user")
    picture = models.ImageField (upload_to='user_pics/', default='user_pics/Default.jpg')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url (self):
        return reverse('user-detail', args=[str(self.id)])


class Event(models.Model):
    eventTitle = models.CharField(max_length=50, help_text="Event Name")
    location = models.CharField(max_length=100, help_text="Location")
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the Event")
    groups = models.ManyToManyField('Group', help_text="Groups this user is associated with")
    host = models.ForeignKey('User',on_delete=models.SET_NULL, null=True)
    events = models.ManyToManyField('Event', help_text="Events created by this user")
    invited = models.ManyToManyField('User', help_text="These users are invited to the group")
    joined = models.ManyToManyField('User', help_text="These users have joined the group")
    picture = models.ImageField(upload_to='user_pics/', default='user_pics/Default.jpg')

    def __str__(self):
        return self.eventTitle


    def get_absolute_url(self):
        """
    Returns the url to access a particular book instance.
    """
        return self.id


class Group(models.Model):
    """
    Model representing a group
    """
    name = models.CharField(max_length=200, help_text="Enter a name for the group")

    description = models.TextField(max_length=1000, help_text="Enter a brief description of the group")

    members = models.ManyToManyField('User', help_text="Select members for this group")

    events = models.ManyToManyField('Event', help_text="Add an event to this group")

    images = models.ImageField(upload_to="")

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('group-detail', args=[str(self.id)])