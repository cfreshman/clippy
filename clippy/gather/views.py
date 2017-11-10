from django.shortcuts import render, get_object_or_404
from .models import Profile, EventGroup, Event
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import is_safe_url
import datetime

def get_viewer_and_context(profile):
    groups = profile.groups.all()
    hosting = profile.hosting.distinct()
    invited = hosting | profile.invited.distinct()
    upcoming = hosting | profile.joined.distinct()
    print(upcoming)
    viewer = {
        'profile': profile,
        'id': profile.id,
        'groups': groups,
        'hosting': hosting,
        'invited': invited,
        'upcoming': upcoming,
    }

    hosting = [e.id for e in hosting]
    joined = filter(lambda e: e.joined.filter(id=profile.id).exists(), invited)
    joined = [e.id for e in joined]
    hidden = [e.id for e in profile.hidden.distinct()]

    context = {
        'viewer': profile,
        'group_list': groups,
        'group_id': 0,
        'event_list': invited,
        'upcoming': upcoming,
        'hosting': hosting,
        'joined': joined,
        'hidden': hidden,
    }

    return viewer, context


# Create your views here.
@login_required
def index(request):
    """
    View function for home page of site.
    """
    viewer, context = get_viewer_and_context(request.user.profile)

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context=context
    )

@login_required
def view_user(request, id):
    if (id == request.user.profile.id):
        return index(request)

    viewer, context = get_viewer_and_context(request.user.profile)

    profile = Profile.objects.get(id=id)
    hosting = profile.hosting.distinct()
    invited = (hosting | profile.invited.distinct()) & viewer['invited']
    upcoming = (hosting | profile.joined.distinct()) & viewer['upcoming']

    return render(
        request,
        'user.html',
        context={**context,
                 'profile': profile,
                 'group_id': -1,
                 'event_list': invited,
                 'upcoming': upcoming,
                 'hidden': []}
    )

@login_required
def view_group(request, id):
    viewer, context = get_viewer_and_context(request.user.profile)

    group = EventGroup.objects.get(id=id)
    members = group.members.exclude(id=viewer['id'])
    events = group.events.all()

    return render(
        request,
        'group.html',
        context={**context,
                 'group': group,
                 'group_id': int(id),
        		 'event_list': events,
        		 'members': members,
                 'hidden': []}
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
            event.hidden.remove(viewer)
        elif reply == 'leave':
            event.joined.remove(viewer)
        elif reply == 'hide':
            event.hidden.add(viewer)
        event.save()

    redirect_to = request.GET.get('next', '')
    if is_safe_url(url=redirect_to, host=request.get_host()):
        return HttpResponseRedirect(redirect_to)

    return render(
        request,
        'event.html',
        context={'viewer': viewer}
    )
