from event.models import Event

event = Event.objects.get(pk=1)
print event.related_to.all()