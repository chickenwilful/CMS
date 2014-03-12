from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import formats
from event.forms import EventCreateForm, EventUpdateForm
from event.models import Event
from jsonutil import json_success


def index(request):
    events = Event.objects.all()
    json_data = {}
    for event in events:
        json_data[event.id] = {
            'id': event.id,
            'title': event.title,
            'created_by': event.created_by.username,
            'created_at': formats.date_format(event.created_at, "SHORT_DATETIME_FORMAT"),
            'description': event.description,
        }
    return json_success(request, {'events': json_data})


def map(request):
    return render(request, 'map.html')


def event_create(request):
    """
    Render and process form to create an event
    """
    if not (request.POST or request.GET):
        form = EventCreateForm()
        return render(request, 'event/event_create.html', {'form': form, 'action': ""})
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
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event/event_retrieve.html', {"event": event})


def event_list(request, emergency_situation_id=0):
    if int(emergency_situation_id) == 0:
        event_list = Event.objects.all()
    else:
        event_list = Event.objects.filter(type=emergency_situation_id)
    return render(request, "event/event_list.html", {'event_list': event_list})


def event_update(request, event_id):
    """
    Render and process a form to edit an Event
    """
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
