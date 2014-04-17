from django.test import TestCase
from django.test.client import Client, RequestFactory
from storm_user.models import UserProfile


class UserViewTest(TestCase):

    fixtures = ['auth.json', 'user.json', 'storm_user.json', 'event.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.client.login(username="admin", password="admin")

    def test_user_create(self):
        response = self.client.get('/user/user_create/')
        self.assertEquals(response.status_code, 200)

    def test_user_retrieve_success(self):
        response = self.client.get('/user/user_retrieve/10/')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['userprofile'].id, 10)

    def test_user_update(self):
        update_url = '/user/user_update/10/'
        response = self.client.get(update_url)
        form = response.context['form']
        data = form.initial
        data["email"] = "email@email.com"
        response = self.client.post(update_url, data)
        #Retrieve again
        response = self.client.get(update_url)
        self.assertEquals(response.status_code, 200)

    def test_user_delete(self):
        response = self.client.get('/user/user_delete/10/')
        self.assertEquals(response.status_code, 302)

    def test_user_list(self):
        response = self.client.get("/user/user_list/")
        self.assertEquals(response.status_code, 200)

