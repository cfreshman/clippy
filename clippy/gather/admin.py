from django.contrib import admin

# Register your models here.
from .models import UserProfile, GroupProfile, Event

admin.site.register(UserProfile)
admin.site.register(GroupProfile)
admin.site.register(Event)
