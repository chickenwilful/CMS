from django.test import TestCase
from event.models import Event


def create_event(title="event", description="desc"):
    return Event.objects.create(title=title, description=description)


class EventViewTest(TestCase):
    def test_event_retrieve(self):
        response = self.client.get('/event/event_retrieve/1/')
        self.assertEqual(response.status_code, 200)

