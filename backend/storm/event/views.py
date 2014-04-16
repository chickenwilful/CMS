import json
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from event.forms import EventCreateForm, EventUpdateForm
from event.models import Event
from main.templatetags.event_permission_tags import can_retrieve_event, can_list_event, can_create_event, can_update_event
from storm_user.models import UserProfile


def map(request):
    event_list = Event.objects.all()
    json_data = {}

    for event in event_list:
        if event.type.name not in json_data:
            json_data[event.type.name] = []
        # Adjustment for local timezone
        created_time = timezone.localtime(event.created_at)
        time = created_time.strftime('%I:%M %p %d/%m/%y')
        json_data[event.type.name].append({
            "postal_code": event.postal_code,
            "reporter": event.reporter_name,
            "time": time,
            "description": event.description,
            "address": event.address,
            "event_link": "/event/event_retrieve/%d/" % event.id
        })
    with open('data.json', 'w') as f:
        json.dump(json_data, f)

    return HttpResponse(json.dumps(json_data), content_type='application/json')


def sendSMS(rescueAgencyList, message):
    #Todo sendSMS()?
    phoneNumberList = []
    for rescueAgency in rescueAgencyList:
        profile = UserProfile.objects.get(user=rescueAgency)
        phoneNumberList.append('65' + profile.phone_number)
        phoneNumberString = (",").join(phoneNumberList)
        print "phoneNumberString: ", "\"", phoneNumberString, "\""

    import urllib

    # If your firewall blocks access to port 5567, you can fall back to port 80:
    # url = "http://bulksms.vsms.net/eapi/submission/send_sms/2/2.0"
    # (See FAQ for more details.)
    url = "http://api.clickatell.com/http/sendmsg?user=vanvoducabc&password=AIGcSRIFaZZVRQ&api_id=3475157&to="+phoneNumberString+"&text=Message"

    print url

    f = urllib.urlopen(url)
     #Read from the object, storing the page's contents in 's'.
    s = f.read()
     #Print the contents
    print s
    f.close()


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
            form.save_m2m()
            sendSMS(model_instance.related_to.all(), model_instance.title)
            return redirect("event.event_list")
        else:
            return render(request, 'event/event_create.html', {'form': form})


def event_retrieve(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    # Check user permissions

    if not can_retrieve_event(request.user, Event.objects.get(pk=event_id)):
        return render(request, "main/no_permission.html")
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
        event_list = Event.objects.all()
    else:
        event_list = Event.objects.filter(type=emergency_situation_id)

    event_list = event_list.order_by('-id')

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
        event = get_object_or_404(Event, pk=event_id)
        form = EventUpdateForm(instance=event)
        return render(request, "event/event_update.html", {'form': form})
    else:
        # Form POST request is submitted
        event = Event.objects.get(pk=event_id)
        form = EventUpdateForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            sendSMS(event.related_to.all(), event.title)
            return HttpResponseRedirect(reverse('event.event_retrieve', args=(event_id,)))
        else:
            return render(request, 'event/event_update.html', {'form': form})


def event_delete(request, event_id):
    """
    delete a post
    """
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return HttpResponseRedirect(reverse('event.event_list'))
