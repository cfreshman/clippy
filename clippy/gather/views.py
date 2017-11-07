from django.shortcuts import render
from .models import UserProfile, GroupProfile, Event

user_id = 5

# Create your views here.
def index(request):
    """
    View function for home page of site.
    """

    viewer = UserProfile.objects.get(id=user_id)
    group_list = viewer.groups.all()
    hosting = viewer.hosting.distinct()
    invited = hosting | viewer.invited.distinct()
    upcoming = hosting | viewer.joined.distinct()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'viewer': viewer,
                 'group_list': group_list, 'group_id': 0,
        		 'event_list': invited,
        		 'upcoming': upcoming},
    )

def user(request, id):
    if (id == user_id):
        return index(request)

    viewer = UserProfile.objects.get(id=user_id)
    group_list = viewer.groups.all()

    user_obj = UserProfile.objects.get(id=id)
    hosting = user_obj.hosting.distinct()
    invited = hosting | user_obj.invited.distinct()
    upcoming = hosting | user_obj.joined.distinct()

    return render(
        request,
        'user.html',
        context={'viewer': viewer,
                 'user': user_obj,
                 'group_list': group_list, 'group_id': -1,
                 'event_list': invited,
                 'upcoming': upcoming},
    )

def group(request, id):
    viewer = UserProfile.objects.get(id=user_id)
    group_list = viewer.groups.all()

    group_obj = GroupProfile.objects.get(id=id)
    members = group_obj.members.exclude(id=user_id)
    events = group_obj.events.all()

    return render(
        request,
        'group.html',
        context={'viewer': viewer,
                 'group': group_obj,
                 'group_list': group_list,'group_id': int(id),
        		 'event_list': events,
        		 'members': members},
    )

def event(request):
    viewer = UserProfile.objects.get(id=user_id)

    return render(
        request,
        'event.html',
        context={'viewer': viewer}
    )

def manager(request):
    viewer = UserProfile.objects.get(id=user_id)
    group_list = viewer.groups.all()

    return render(
        request,
        'manager.html',
        context={'viewer': viewer,
                 'group_list': group_list, 'group_id': -1,}
    )

def settings(request):
    viewer = UserProfile.objects.get(id=user_id)

    return render(
        request,
        'settings.html',
        context={'viewer': viewer}
    )