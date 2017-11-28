from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, EventGroup, Event
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import is_safe_url
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def get_viewer_and_context(profile):
    groups = profile.groups.all()
    hosting = profile.hosting.distinct()
    invited = hosting | profile.invited.distinct()
    for group in groups:
        invited |= group.events.distinct()
    upcoming = hosting | profile.joined.distinct()
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
    groups = profile.groups.all()
    is_friend = viewer['profile'] in profile.friends.all()
    hosting = profile.hosting.distinct()
    invited = (hosting | profile.invited.distinct())
    for group in groups:
        invited |= group.events.distinct()
    invited &= viewer['invited']
    upcoming = (hosting | profile.joined.distinct()) & viewer['upcoming']

    return render(
        request,
        'user.html',
        context={**context,
                 'profile': profile,
                 'group_id': -1,
                 'is_friend': is_friend,
                 'event_list': invited,
                 'upcoming': upcoming,
                 'hidden': []}
    )

@login_required
def view_group(request, id):
    viewer, context = get_viewer_and_context(request.user.profile)

    group = EventGroup.objects.get(id=id)
    members = group.members.all()
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
    viewer, context = get_viewer_and_context(request.user.profile)

    event = Event.objects.get(id=id)
    going = (event.joined.all() | event.hosts.all()).distinct()
    events = Event.objects.filter(id=id)

    return render(
        request,
        'event.html',
        context={**context,
                 'event': event,
                 'group_id': -1,
                 'event_list': events,
                 'going': going,
                 'hidden': []}
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


@method_decorator(login_required, name='dispatch')
class GroupCreate(CreateView):
    model = EventGroup
    fields = '__all__'

    def get_form(self, form_class=None):    
        form = super(GroupCreate, self).get_form(form_class)
        form.fields['members'].queryset = self.request.user.profile.friends.distinct()
        return form

    def form_valid(self, form):
        form.cleaned_data['members'] |= Profile.objects.filter(id=self.request.user.profile.id).distinct()
        return super(GroupCreate, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class GroupEdit(UpdateView):
    model = EventGroup
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.profile in self.object.members.all():
            return HttpResponseRedirect(self.object.get_absolute_url())
        return super(GroupEdit, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):  
        form = super(GroupEdit, self).get_form(form_class)
        form.fields['members'].queryset = (self.object.members.exclude(id=self.request.user.profile.id) 
                                           | self.request.user.profile.friends.all()).distinct()
        return form

    def form_valid(self, form):
        form.cleaned_data['members'] |= Profile.objects.filter(id=self.request.user.profile.id).distinct()
        return super(GroupEdit, self).form_valid(form)


@login_required
def create_event(request):
    viewer = request.user.profile

    return render(
        request,
        'create_event.html',
        context={'viewer': viewer}
    )

@method_decorator(login_required, name='dispatch')
class EventCreate(CreateView):
    model = Event
    fields = ['title', 'location', 'time', 'description', 'picture', 'groups', 'hosts', 'invited']

    def get_form(self, form_class=None):    
        form = super(EventCreate, self).get_form(form_class)
        for field in ['title', 'location', 'time', 'description']:
            form.fields[field].help_text = ''
        form.fields['time'].widget.attrs['placeholder'] = 'MM/DD/YYYY HH:MM:SS'
        form.fields['groups'].queryset = self.request.user.profile.groups.distinct()
        form.fields['groups'].help_text = 'Select groups to invite to the event'
        form.fields['hosts'].required = False
        form.fields['hosts'].queryset = self.request.user.profile.friends.distinct()
        form.fields['hosts'].help_text = 'Select additional hosts for the event'
        form.fields['invited'].queryset = self.request.user.profile.friends.distinct()
        form.fields['invited'].help_text = 'Select individuals users to invite to the event'
        return form

    def form_valid(self, form):
        form.cleaned_data['hosts'] |= Profile.objects.filter(id=self.request.user.profile.id).distinct()
        form.save()
        return super(EventCreate, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class EventEdit(UpdateView):
    model = Event
    fields = ['title', 'location', 'time', 'description', 'picture', 'groups', 'hosts', 'invited']

    def get_form(self, form_class=None):    
        form = super(EventEdit, self).get_form(form_class)
        for field in ['title', 'location', 'time', 'description']:
            form.fields[field].help_text = ''
        form.fields['time'].widget.attrs['placeholder'] = 'YYYY-MM-DD HH:MM:SS'
        form.fields['groups'].queryset = self.request.user.profile.groups.distinct()
        form.fields['groups'].help_text = 'Select groups to invite to the event'
        form.fields['hosts'].required = False
        form.fields['hosts'].queryset = self.request.user.profile.friends.distinct()
        form.fields['hosts'].help_text = 'Select additional hosts for the event'
        form.fields['invited'].queryset = self.request.user.profile.friends.distinct()
        form.fields['invited'].help_text = 'Select individuals users to invite to the event'
        return form

    def form_valid(self, form):
        form.cleaned_data['hosts'] |= Profile.objects.filter(id=self.request.user.profile.id).distinct()
        form.save()
        return super(EventEdit, self).form_valid(form)

class ProfileEdit(UpdateView):
    model = Profile

    fields = ['friends', 'picture']
    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


@login_required
def edit_event(request, id):
    viewer = request.user.profile

    return render(
        request,
        'create_event.html',
        context={'viewer': viewer}
    )


@login_required
def user_action(request, id, action):
    viewer = request.user.profile

    profile = get_object_or_404(Profile, id=id)

    redirect_to = request.GET.get('next', '')
    if is_safe_url(url=redirect_to, host=request.get_host()):
        return HttpResponseRedirect(redirect_to)
    return view_user(request, id)

@login_required
def group_action(request, id, action):
    viewer = request.user.profile

    group = get_object_or_404(EventGroup, id=id)

    redirect_to = request.GET.get('next', '')
    if is_safe_url(url=redirect_to, host=request.get_host()):
        return HttpResponseRedirect(redirect_to)
    return view_group(request, id)

@login_required
def event_action(request, id, action):
    viewer = request.user.profile

    event = get_object_or_404(Event, id=id)
    if event.invited.filter(id=viewer.id).exists():
        if action == 'join':
            event.joined.add(viewer)
            event.hidden.remove(viewer)
        elif action == 'leave':
            event.joined.remove(viewer)
        elif action == 'hide':
            event.hidden.add(viewer)
        event.save()

    redirect_to = request.GET.get('next', '')
    if is_safe_url(url=redirect_to, host=request.get_host()):
        return HttpResponseRedirect(redirect_to)
    return view_event(request, id)

from .forms import SearchForm
@login_required
def search(request):
    viewer = request.user.profile

    form = SearchForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        user = get_object_or_404(User, username=username)
        return HttpResponseRedirect(user.profile.get_absolute_url())
    return HttpResponseRedirect(reverse('index'))
