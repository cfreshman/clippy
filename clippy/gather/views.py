from django.shortcuts import render, get_object_or_404
from .models import Profile, EventGroup, Event
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import is_safe_url
import datetime

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

    hosting = [e.id for e in hosting]

    joined = filter(lambda e: e.joined.filter(id=viewer.id).exists(), invited)
    joined = [e.id for e in joined]

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'viewer': viewer,
                 'group_list': group_list, 'group_id': 0,
        		 'event_list': invited,
        		 'upcoming': upcoming,
                 'hosting': hosting, 'joined': joined,}
    )

@login_required
def view_user(request, id):
    viewer = request.user.profile
    hosting = viewer.hosting.distinct()
    if (id == viewer.id):
        return index(request)

    group_list = viewer.groups.all()

    profile = Profile.objects.get(id=id)
    other_hosting = profile.hosting.distinct()
    invited = ((other_hosting | profile.invited.distinct()) 
        & (hosting | viewer.invited.distinct()))
    upcoming = ((other_hosting | profile.joined.distinct()) 
        & (hosting | viewer.joined.distinct()))

    joined = filter(lambda e: e.joined.filter(id=viewer.id).exists(), invited)
    joined = map(lambda e: e.id, joined)

    return render(
        request,
        'user.html',
        context={'viewer': viewer,
                 'profile': profile,
                 'group_list': group_list, 'group_id': -1,
                 'event_list': invited,
                 'upcoming': upcoming,
                 'joined': joined,}
    )

@login_required
def view_group(request, id):
    viewer = request.user.profile
    group_list = viewer.groups.all()

    group_obj = EventGroup.objects.get(id=id)
    members = group_obj.members.exclude(id=viewer.id)
    events = group_obj.events.all()

    joined = filter(lambda e: e.joined.filter(id=viewer.id).exists(), events)
    joined = map(lambda e: e.id, joined)

    return render(
        request,
        'group.html',
        context={'viewer': viewer,
                 'group': group_obj,
                 'group_list': group_list,'group_id': int(id),
        		 'event_list': events,
        		 'members': members,
                 'joined': joined,}
    )

@login_required
def view_event(request, id):
    viewer = request.user.profile

    return render(
        request,
        'event.html',
        context={'viewer': viewer}
    )


@login_required
def create_group(request):
    viewer = request.user.profile
    group_list = viewer.groups.all()

    return render(
        request,
        'manager.html',
        context={'viewer': viewer,
                 'group_list': group_list, 'group_id': -1}
    )

@login_required
def create_event(request):
    viewer = request.user.profile

    return render(
        request,
        'event.html',
        context={'viewer': viewer}
    )


@login_required
def settings(request):
    viewer = request.user.profile

    return render(
        request,
        'settings.html',
        context={'viewer': viewer}
    )

@login_required
def edit_group(request, id):
    viewer = request.user.profile
    group_list = viewer.groups.all()

    return render(
        request,
        'manager.html',
        context={'viewer': viewer,
                 'group_list': group_list, 'group_id': id}
    )

@login_required
def edit_event(request, id):
    viewer = request.user.profile

    return render(
        request,
        'event.html',
        context={'viewer': viewer}
    )


@login_required
def event_reply(request, id, reply):
    viewer = request.user.profile

    event = get_object_or_404(Event, id=id)
    if event.invited.filter(id=viewer.id).exists():
        if reply == 'join':
            event.joined.add(viewer)
        elif reply == 'leave':
            event.joined.remove(viewer)
        elif reply == 'hide':
            event.invited.remove(viewer)
        event.save()

    redirect_to = request.GET.get('next', '')
    if is_safe_url(url=redirect_to, host=request.get_host()):
        return HttpResponseRedirect(redirect_to)

    return render(
        request,
        'event.html',
        context={'viewer': viewer}
    )
