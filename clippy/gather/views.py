from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Profile, EventGroup, Event
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import is_safe_url
import datetime
from django.contrib import messages
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
        return super(EventEdit, self).form_valid(form)

from .forms import EditProfileForm
from django.contrib.auth.models import User
from django.db import IntegrityError
@login_required
def edit_profile(request):
    profile = request.user.profile
    user = request.user
    form = EditProfileForm(request.POST or None, request.FILES or None,
                                                 initial={'first_name':user.first_name, 
                                                          'last_name':user.last_name,
                                                          'username':user.get_username(),
                                                          'picture':profile.picture})
    if request.method == 'POST':
        if form.is_valid():
            if (user.first_name != request.POST['first_name'] or
                user.last_name != request.POST['last_name']):
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                messages.add_message(request, messages.SUCCESS, "Name changed to " + 
                    user.first_name + " " + user.last_name)
            if user.username != request.POST['username']:
                temp = user.username
                try:
                    user.username = request.POST['username']
                    user.save()
                    messages.add_message(request, messages.SUCCESS, "Username changed to " + 
                        user.username)
                except IntegrityError:
                    user.username = temp
                    messages.add_message(request, messages.ERROR, "Invalid username.")
            user.save()
            if request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                messages.success(request, "Profile picture changed.")

            return HttpResponseRedirect('%s'%(reverse('settings')))

    context = {
        "form": form
    }
 
    return render(request, "profile_form.html", context)

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if not request.user.is_authenticated():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, "Something didn't match. Check requirements below:")
            messages.info(request,
                """Your password can't be too similar to your other personal information.<br>
                Your password must contain at least 8 characters.<br>
                Your password can't be a commonly used password.<br>
                Your password can't be entirely numeric.""", extra_tags='safe')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@login_required
def edit_event(request, id):
    viewer = request.user.profile

@login_required
def user_action(request, id, action):
    viewer = request.user.profile

    profile = get_object_or_404(Profile, id=id)

    if action == 'unfriend':
        profile.friends.remove(viewer)
    elif action == 'friend':
        profile.friends.add(viewer)

    redirect_to = request.GET.get('next', '')
    if is_safe_url(url=redirect_to, host=request.get_host()):
        return HttpResponseRedirect(redirect_to)
    return view_user(request, id)

@login_required
def group_action(request, id, action):
    viewer = request.user.profile

    group = get_object_or_404(EventGroup, id=id)

    if action == 'leave':
        group.members.remove(viewer)

    redirect_to = request.GET.get('next', '')
    if is_safe_url(url=redirect_to, host=request.get_host()):
        return HttpResponseRedirect(redirect_to)
    return view_group(request, id)

@login_required
def event_action(request, id, action):
    viewer = request.user.profile

    event = get_object_or_404(Event, id=id)
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
