from django.shortcuts import render
from .models import Profile, EventGroup, Event
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    """
    View function for home page of site.
    """

    viewer = request.user.profile
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

@login_required
def user(request, id):
    viewer = request.user.profile
    if (id == viewer.id):
        return index(request)

    group_list = viewer.groups.all()

    profile = Profile.objects.get(id=id)
    hosting = profile.hosting.distinct()
    invited = hosting | profile.invited.distinct()
    upcoming = hosting | profile.joined.distinct()

    return render(
        request,
        'user.html',
        context={'viewer': viewer,
                 'profile': profile,
                 'group_list': group_list, 'group_id': -1,
                 'event_list': invited,
                 'upcoming': upcoming},
    )

@login_required
def group(request, id):
    viewer = request.user.profile
    group_list = viewer.groups.all()

    group_obj = EventGroup.objects.get(id=id)
    members = group_obj.members.exclude(id=viewer.id)
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

@login_required
def event(request):
    viewer = request.user.profile

    return render(
        request,
        'event.html',
        context={'viewer': viewer}
    )

@login_required
def manager(request):
    viewer = request.user.profile
    group_list = viewer.groups.all()

    return render(
        request,
        'manager.html',
        context={'viewer': viewer,
                 'group_list': group_list, 'group_id': -1,}
    )

@login_required
def settings(request):
    viewer = request.user.profile

    return render(
        request,
        'settings.html',
        context={'viewer': viewer}
    )
