from django.test import TestCase
from event.models import Event


class EventViewTest(TestCase):

    def test_event_create(self):
        pass

    def test_event_retrieve_success(self):
        response = self.client.get('/event/event_retrieve/1/')
        self.assertEqual(response.status_code, 200)

    def test_event_retrieve_fail(self):
        response = self.client.get()

    def test_event_update(self):
        pass

    def test_event_delete(self):
        pass

    def test_event_list(self):

