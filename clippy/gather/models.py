from django.db import models

# Create your models here.
class User (models.Model):
	# Fields
	first_name = models.CharField (max_length=50, help_text="First Name")
	last_name = models.CharField (max_length=50, help_text="Last Name")
	groups = models.ManyToManyField (Group, help_text="Groups this user is associated with")
	events = models.ManyToManyField (Event, help_text="Events created by this user")
	friends = models.ManyToManyField (User, help_text="Friends of this user")
	picture = models.ImageField (upload_to='user_pics/', default='user_pics/Default.jpg')

	def __str__(self):
		return '%s %s' % (self.first_name, self.last_name)

	def get_absolute_url (self):
		return reverse('user-detail', args=[str(self.id)])