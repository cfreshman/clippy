from django.shortcuts import render
from .models import User, Group, Event

user_id = 6

# Create your views here.
def index(request):
    """
    View function for home page of site.
    """

    viewer = User.objects.get(id=user_id)
    group_list = viewer.groups.all()
    invited = viewer.invited.all()
    upcoming = viewer.joined.all()

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

    viewer = User.objects.get(id=user_id)

    user_obj = User.objects.get(id=id)
    group_list = user_obj.groups.all()
    invited = user_obj.invited.all()
    upcoming = user_obj.joined.all()

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
    viewer = User.objects.get(id=user_id)
    group_list = viewer.groups.all()

    group_obj = Group.objects.get(id=id)
    members = group_obj.members.all()
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
    viewer = User.objects.get(id=user_id)

    return render(
        request,
        'event.html',
        context={'viewer': viewer}
    )

def manager(request):
    viewer = User.objects.get(id=user_id)
    group_list = viewer.groups.all()

    return render(
        request,
        'manager.html',
        context={'viewer': viewer,
                 'group_list': group_list, 'group_id': -1,}
    )

def settings(request):
    viewer = User.objects.get(id=user_id)

    return render(
        request,
        'settings.html',
        context={'viewer': viewer}
    )