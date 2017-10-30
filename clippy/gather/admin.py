from django.contrib import admin

# Register your models here.
from .models import User, Group, Event

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Event)
