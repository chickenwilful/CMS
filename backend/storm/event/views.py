from itertools import chain
import json
from django.db.models import Q
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from event.forms import EventCreateForm, EventUpdateForm
from event.models import Event
from jsonutil import json_success
from main.templatetags.event_permission_tags import can_retrieve_event, can_list_event, can_create_event, can_update_event


def map(request):
    event_list = Event.objects.all()
    json_data = {}

    for event in event_list:
        if event.type.name not in json_data:
            json_data[event.type.name] = []
        json_data[event.type.name].append({
            "postal_code": event.postal_code,
            "reporter": event.caller_name,
            "time": event.created_at.strftime('%Y-%m-%d %H:%M'),
            "description": event.description,
            "address": event.address,
        })

    with open('data.json', 'w') as f:
        json.dump(json_data, f)

    return json_success(request, {'events': json_data})


def event_create(request):
    """
    Render and process form to create an event
    """
    #check user permissions
    if not can_create_event(request.user):
        return render(request, "main/no_permission.html")

    if not (request.POST or request.GET):
        form = EventCreateForm()
        return render(request, 'event/event_create.html', {'form': form})
    else:
        #Form POST request is submitted
        form = EventCreateForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.created_by_id = request.user.id
            model_instance.created_at = timezone.now()
            model_instance.save()
            return redirect("event.event_list")
        else:
            return render(request, 'event/event_create.html', {'form': form})


def event_retrieve(request, event_id):
    # Check user permissions
    if not can_retrieve_event(request.user, Event.objects.get(pk=event_id)):
        return render(request, "main/no_permission.html")
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event/event_retrieve.html', {"event": event})


def event_list(request, emergency_situation_id=0):
    """
    List all events from database, which can be seen by current user.
    Users can see all events that are related to them, or they are admins
    """
    # Check user permissions
    if not can_list_event(request.user):
        return render(request, "main/no_permission.html")

    #Query database
    if int(emergency_situation_id) == 0:
        temp = Event.objects.all()
    else:
        temp = Event.objects.filter(type=emergency_situation_id)

    if not "CMSAdmin" in request.user.groups.all():
        event_list = temp.filter(Q(created_by=request.user) | Q(related_to=request.user))
    else:
        event_list = temp

    # Make Response
    for event in event_list:
        event.description = event.description[:250]
    return render(request, "event/event_list.html", {'event_list': event_list, 'filter_id': emergency_situation_id})


def event_update(request, event_id):
    """
    Render and process a form to edit an Event
    """
    #Check permission
    if not can_update_event(request.user, Event.objects.get(pk=event_id)):
        return render(request, "main/no_permission.html")

    #Handle request
    if not (request.POST or request.GET):
        post = get_object_or_404(Event, pk=event_id)
        form = EventUpdateForm(instance=post)
        return render(request, "event/event_update.html", {'form': form})
    else:
        # Form POST request is submitted
        event = Event.objects.get(pk=event_id)
        form = EventUpdateForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('event.event_retrieve', args=(event_id,)))
        else:
            return HttpResponse("Fail!")


def event_delete(request, event_id):
    """
    delete a post
    """
    Event.objects.get(pk=event_id).delete()
    return HttpResponseRedirect(reverse('event.event_list'))
