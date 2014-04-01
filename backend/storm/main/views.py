from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.shortcuts import render, redirect
from event.models import Event
from main.templatetags.event_permission_tags import can_list_event


def main_page(request, emergency_situation_id=0):
    """
    List all events from database, which can be seen by current user.
    Users can see all events that are related to them, or they are admins
    """
    return redirect("/event/event_list/")
    # Check user permissions
    if not can_list_event(request.user):
        return render(request, "main/main_page.html",
                      {'event_list': [], 'filter_id': emergency_situation_id})

    #Query database
    if int(emergency_situation_id) == 0:
        event_list = Event.objects.all()
    else:
        event_list = Event.objects.filter(type=emergency_situation_id)

    # if not Group.objects.get(name="CMSAdmin") in request.user.groups.all():
    #     event_list = event_list.filter(Q(created_by=request.user) | Q(related_to=request.user))
    event_list = event_list.order_by('-id')
    # Make Response
    for event in event_list:
        event.description = event.description[:250] #Todo Need to use tags instead
    return render(request, "main/main_page.html",
                  {'event_list': event_list, 'filter_id': emergency_situation_id})


def aboutus(request):
    return render(request, "main/about.html")


def contactus(request):
    return render(request, "main/Contact.html")



