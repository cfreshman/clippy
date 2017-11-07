from django.contrib import admin

# Register your models here.
from .models import Profile, EventGroup, Event

admin.site.register(Profile)
admin.site.register(EventGroup)
admin.site.register(Event)
