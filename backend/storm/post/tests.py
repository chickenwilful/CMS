from django.test import TestCase
from post.forms import PostCreateForm
from django.test.client import Client, RequestFactory
from post.models import Post


class postViewTest(TestCase):

    fixtures = ['auth.json', 'post.json', 'storm_user.json', 'event.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.post = Post(type_id=2,
                         title="test_title",
                         content="test_content",
                         created_by_id=8,
                         created_at="2014-03-26 15:33:06",
                         isPublished=True)
        self.client.login(username="admin", password="admin")

    def test_post_create(self):
        form = PostCreateForm(instance=self.post)
        response = self.client.post('/post/post_create/', {'form': form})
        self.assertEquals(response.status_code, 200)

    def test_post_retrieve_success(self):
        response = self.client.get('/post/post_retrieve/10/')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['post'].id, 10)

    def test_post_retrieve_fail(self):
        # response = self.client.get('/post/post_retrieve/1/')
        # self.assertEquals(response.status_code, 404)
        pass
    
    def test_post_update(self):
        update_url = '/post/post_update/10/'
        response = self.client.get(update_url)
        form = response.context['form']
        data = form.initial
        data["title"] = "New title"
        self.client.post(update_url, data)
        #Retrieve again
        response = self.client.get(update_url)
        self.assertContains(response, "New title")
        self.assertEquals(response.context['form'].initial['title'], 'New title')

    def test_post_delete(self):
        response = self.client.get('/post/post_delete/10/')
        self.assertEquals(response.status_code, 302)

    def test_post_list(self):
        response = self.client.get("/post/post_list/")
        self.assertEquals(response.status_code, 200)

