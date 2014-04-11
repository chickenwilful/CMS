from django.test import TestCase
from event.forms import EventCreateForm
from event.models import Event
from django.test.client import Client, RequestFactory


class EventViewTest(TestCase):

    fixtures = ['auth.json', 'event.json', 'storm_user.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.event = Event(type_id=2,
                           title="test_title",
                           created_by_id=8,
                           created_at="2014-03-26 15:33:06",
                           reporter_name="test_reporter_name",
                           reporter_phone_number="12345",
                           postal_code="654321",
                           address="test_address")
        self.client.login(username="admin", password="admin")

    def test_event_create(self):
        form = EventCreateForm(instance=self.event)
        response = self.client.post('/event/event_create/', {'form': form})
        self.assertEquals(response.status_code, 200)

    def test_event_retrieve_success(self):
        response = self.client.get('/event/event_retrieve/7/')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['event'].id, 7)

    def test_event_retrieve_fail(self):
        # response = self.client.get('/event/event_retrieve/1/')
        # self.assertEquals(response.status_code, 404)
        pass
    
    def test_event_update(self):
        update_url = '/event/event_update/7/'
        response = self.client.get(update_url)
        form = response.context['form']
        data = form.initial
        data["title"] = "New title"
        response = self.client.post(update_url, data)
        #Retrieve again
        response = self.client.get(update_url)
        self.assertContains(response, "New title")
        self.assertEquals(response.context['form'].initial['title'], 'New title')

    def test_event_delete(self):
        response = self.client.get('/event/event_delete/7/')
        self.assertEquals(response.status_code, 302)

    def test_event_list(self):
        response = self.client.get("/event/event_list/")
        self.assertEquals(response.status_code, 200)

