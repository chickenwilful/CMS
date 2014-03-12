from django.test import TestCase
import random
import string
import urllib

from socialnetwork.socialbot import SocialBot
from socialnetwork.socialcenter import SocialCenter

def generate_random_string(size, chars):
    return ''.join(random.choice(chars) for _ in range(size))

class TestBot(SocialBot):

    def post(self, title, content, link):
        result = {}
        if not any(title, content):
            result["error"] = "No content in post."
        else:
            if title:
                result["title"] = title
            if content:
                result["content"] = content
            if link:
                result["link"] = link
                
        return result
    
    def authenticate(self, token, sub_token=None):
        self.main_token = token
        self.sub_token = sub_token
        
        result = {"main_token" : token}
        if sub_token:
            result["sub_token"] = sub_token
        return result
        
    def refresh_token(self):
        pass
    
    def start_authentication(self, callback_url):
        test_auth_data = {"state": "test_state"}
        return "http://test.com/auth?redirect_uri=%s" % urllib.quote_plus(callback_url), test_auth_data
    
    def process_token(self, client_token, **kwargs):
        result = {}
        
        if client_token != "valid_code":
            result["error"] = "Invalid code"
        else:
            result["main_token"] = "test_main_token"
        
        pass
    
    def get_pages(self, request_token):
        pages = []
        if request_token == "valid_request_token":
            for num in range(10):
                pages.append({ id: "%d" % num, name: "Page %d" % num })
        return pages
    
    def clear_token(self):
        if hasattr(self, "main_token"):
            del self.main_token
        if hasattr(self, "sub_token"):
            del self.sub_token

class SocialCenterTest(TestCase):

    TEST_SITE = "test"
    
    def setUp(self):
        self.test_bot = TestBot()
        self.social_center = SocialCenter()
        self.social_center.add_site(self.TEST_SITE, self.test_bot)
    
    def test_social_center_is_singleton(self):
        social_center = SocialCenter()
        self.assertTrue(self.social_center is social_center)
    
    def test_social_center_only_accepts_social_bots(self):
        self.assertRaises(ValueError, self.social_center.add_site, "invalid site", 434)
        self.assertRaises(ValueError, self.social_center.add_site, 1342, TestBot())
    
    def test_social_bot_is_logged_out(self):
        self.assertFalse(self.social_center.is_logged_in(self.TEST_SITE))
    
    def test_social_bot_can_authenticate(self):
        self.social_center.authenticate(self.TEST_SITE, "test_main_token", "test_sub_token")
        self.assertEqual(self.test_bot.main_token, "test_main_token")
        self.assertEqual(self.test_bot.sub_token, "test_sub_token")
        self.assertTrue(self.social_center.is_logged_in(self.TEST_SITE))
    
    def test_social_bot_can_start_auth(self):
        callback_url = "http://testapp.com/"
        
        redirect_url, auth_data = self.social_center.start_authentication(self.TEST_SITE, callback_url)
        
        self.assertEqual(redirect_url, "http://test.com/auth?redirect_uri=%s" % urllib.quote_plus(callback_url))
        self.assertEqual(auth_data["state"], "test_state")
