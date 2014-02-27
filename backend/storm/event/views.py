from django.shortcuts import render, get_object_or_404
from django.utils import formats
from event.forms import EventCreateForm
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
    if not (request.POST or request.GET):
        form = EventCreateForm()
        return render(request, 'post/post_create.html', {'form': form, 'action': ""})
    else:
        #Form POST request is submitted
        form = EventCreateForm(request.POST)
        if form.is_valid():
            pass
        else:
            pass
    pass


def event_retrieve(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event/event_retrieve.html', {'event': event})


def event_list(request):
    event_list = request.user.related.all()
    return render(request, "event/event_list.html", {'event_list': event_list})