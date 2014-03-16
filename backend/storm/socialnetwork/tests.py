from django.test import TestCase
from django.http import HttpRequest, HttpResponseRedirect
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
import random
import string
import urllib
import copy

import socialnetwork.views as sn_views
from socialnetwork.socialbot import SocialBot
from socialnetwork.socialcenter import SocialCenter

class TestBot(SocialBot):
    """Implementation of SocialBot for tests
    """
    __client_token_name = "test_code"
    
    # Exposed fields, so that tests can use them for comparisons
    _session_token = "fjsd0hnf02HNR)"
    _valid_client_token = "valid_code"
    _valid_main_token = "test_main_token"
    
    def must_refresh_token(self):
        return False
    
    def must_select_page(self):
        return False
    
    def get_site_name(self):
        return "Test Site"
    
    def get_client_token_name(self):
        return self.__client_token_name
    
    def get_account_name(self):
        if hasattr(self, "main_token"):
            return "Test Site Account"
        return "Unauthorized"
    
    def get_account_url(self):
        if hasattr(self, "main_token"):
            return "https://test.com/page"
        return "Unauthorized"
    
    def post(self, title, content, link):
        result = {}
        if not (title or content):
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
        auth_data = {}
        
        auth_data["session_token"] = self._session_token
        auth_data["callback_url"] = callback_url
        
        return "http://test.com/auth?redirect_uri=%s" % urllib.quote_plus(callback_url), auth_data
    
    def process_token(self, client_token, auth_data):
        result = {}
        
        # These assignments will crash tests if the keys don't exist
        session_token = auth_data["session_token"]
        callback_url = auth_data["callback_url"]
        
        if session_token != self._session_token:
            result["error"] = "Invalid session token"
        elif client_token != self._valid_client_token:
            result["error"] = "Invalid code"
        else:
            result["main_token"] = self._valid_main_token
        
        return result
    
    def get_pages(self, request_token):
        raise NotImplementedError("This SocialBot has no pages.")
    
    def clear_token(self):
        if hasattr(self, "main_token"):
            del self.main_token
        if hasattr(self, "sub_token"):
            del self.sub_token

class TestBotWithPages(TestBot):
    """Implementation of SocialBot for tests
    """
    
    def must_select_page(self):
        return True
    
    def get_site_name(self):
        return "Test Paged Site"
    
    def get_account_name(self):
        if hasattr(self, "main_token"):
            return "Test Paged Site Account"
        return "Unauthorized"
    
    def get_account_url(self):
        if hasattr(self, "_main_token"):
            return "https://testpaged.com/page"
        return "Unauthorized"
    
    def get_pages(self, request_token):
        pages = []
        if request_token == self._valid_main_token:
            for num in range(10):
                pages.append({ "id" : "%d" % (num+1), "name" : "Page %d" % (num+1) })
        return pages

class SocialCenterTest(TestCase):

    TEST_SITE = "test"
    TEST_PAGED_SITE = "test_paged"
    
    @classmethod
    def setUpClass(self):
        self.test_bot = TestBot()
        self.test_paged_bot = TestBotWithPages()
        self.social_center = SocialCenter()
        self.social_center.add_site(self.TEST_SITE, self.test_bot)
        self.social_center.add_site(self.TEST_PAGED_SITE, self.test_paged_bot)
    
    @classmethod
    def tearDownClass(self):
        self.social_center.logout(self.TEST_SITE)
        self.social_center.logout(self.TEST_PAGED_SITE)
        
        self.social_center.remove_site(self.TEST_SITE)
        self.social_center.remove_site(self.TEST_PAGED_SITE)
        
        del self.social_center
        del self.test_bot
        del self.test_paged_bot
    
    def test_social_center_is_singleton(self):
        social_center = SocialCenter()
        self.assertIs(self.social_center, social_center)
    
    def test_social_center_only_accepts_social_bots(self):
        self.assertRaises(ValueError, self.social_center.add_site, "invalid site", 434)
        self.assertRaises(ValueError, self.social_center.add_site, 1342, TestBot())
    
    def test_social_center_has_test_bots(self):
        self.assertTrue(self.social_center.has_site(self.TEST_SITE))
        self.assertTrue(self.social_center.has_site(self.TEST_PAGED_SITE))
    
    def test_social_center_can_remove_bots(self):
        self.social_center.remove_site(self.TEST_SITE)
        self.assertFalse(self.social_center.has_site(self.TEST_SITE))
        
        self.social_center.add_site(self.TEST_SITE, self.test_bot)
    
    def test_social_center_returns_test_bots(self):
        sites = self.social_center.get_sites()
        
        self.assertIn(self.TEST_SITE, sites)
        self.assertIn(self.TEST_PAGED_SITE, sites)
        
        self.assertEqual(sites[self.TEST_SITE]["name"], self.test_bot.get_site_name())
        self.assertEqual(sites[self.TEST_PAGED_SITE]["name"], self.test_paged_bot.get_site_name())
    
    def test_social_center_can_return_bot_properties(self):
        #import pdb; pdb.set_trace()
        self.assertEqual(self.social_center.must_select_page(self.TEST_SITE),
                         self.test_bot.must_select_page())
        self.assertEqual(self.social_center.must_select_page(self.TEST_PAGED_SITE),
                         self.test_paged_bot.must_select_page())
        
        self.assertEqual(self.social_center.get_site_name(self.TEST_SITE),
                         self.test_bot.get_site_name())
        self.assertEqual(self.social_center.get_site_name(self.TEST_PAGED_SITE),
                         self.test_paged_bot.get_site_name())
        
        self.assertEqual(self.social_center.get_client_token_name(self.TEST_SITE),
                         self.test_bot.get_client_token_name())
        self.assertEqual(self.social_center.get_client_token_name(self.TEST_PAGED_SITE),
                         self.test_paged_bot.get_client_token_name())
        
        self.assertEqual(self.social_center.get_account_name(self.TEST_SITE),
                         self.test_bot.get_account_name())
        self.assertEqual(self.social_center.get_account_name(self.TEST_PAGED_SITE),
                         self.test_paged_bot.get_account_name())
        
        self.assertEqual(self.social_center.get_account_url(self.TEST_SITE),
                         self.test_bot.get_account_url())
        self.assertEqual(self.social_center.get_account_url(self.TEST_PAGED_SITE),
                         self.test_paged_bot.get_account_url())
    
    def test_social_bot_is_initially_logged_out(self):
        self.assertFalse(self.social_center.is_logged_in(self.TEST_SITE))
        self.assertFalse(self.social_center.is_logged_in(self.TEST_PAGED_SITE))
    
    def test_social_bot_can_authenticate(self):
        self.social_center.authenticate(self.TEST_SITE, "test_main_token", "test_sub_token")
        
        self.assertEqual(self.test_bot.main_token, "test_main_token")
        self.assertEqual(self.test_bot.sub_token, "test_sub_token")
        self.assertTrue(self.social_center.is_logged_in(self.TEST_SITE))
    
    def test_social_bot_can_start_auth(self):
        callback_url = "http://testapp.com/"
        
        redirect_url, auth_data = self.social_center.start_authentication(self.TEST_SITE, callback_url)
        
        self.assertEqual(redirect_url, "http://test.com/auth?redirect_uri=%s" % urllib.quote_plus(callback_url))
        self.assertEqual(auth_data["session_token"], self.test_bot._session_token)
        self.assertEqual(auth_data["callback_url"], callback_url)
        
    def test_social_bot_can_process_client_token(self):
        callback_url = "http://testapp2.com/"
        redirect_url, auth_data = self.social_center.start_authentication(self.TEST_SITE, callback_url)
        
        self.assertRaises(BaseException, self.social_center.process_client_token, None)
        self.assertRaises(BaseException, self.social_center.process_client_token, {})
        self.assertRaises(BaseException, self.social_center.process_client_token, { "callback_url" : callback_url })
        
        invalid_result = self.social_center.process_client_token(self.TEST_SITE, "invalid_code", auth_data)
        
        self.assertNotIn("main_token", invalid_result)
        self.assertIn("error", invalid_result)
        
        modified_data = auth_data.copy()
        modified_data["session_token"] = "invalidSessionToken"
        modified_result = self.social_center.process_client_token(self.TEST_SITE, self.test_bot._valid_client_token, modified_data)
        
        self.assertNotIn("main_token", modified_result)
        self.assertIn("error", modified_result)
        
        valid_result = self.social_center.process_client_token(self.TEST_SITE, self.test_bot._valid_client_token, auth_data)
        
        self.assertIn("main_token", valid_result)
        self.assertNotIn("error", valid_result)
    
    def test_only_paged_bot_has_pages(self):
        self.assertFalse(self.social_center.must_select_page(self.TEST_SITE))
        self.assertTrue(self.social_center.must_select_page(self.TEST_PAGED_SITE))
        
        self.assertRaises(NotImplementedError, self.social_center.get_pages, self.TEST_SITE, "any_token")
        # Should not raise any errors:
        pages = self.social_center.get_pages(self.TEST_PAGED_SITE, self.test_paged_bot._valid_main_token)
    
    def test_social_bot_can_get_pages(self):
        self.social_center.authenticate(self.TEST_PAGED_SITE, "test_main_token", "test_sub_token")
        
        invalid_pages = self.social_center.get_pages(self.TEST_PAGED_SITE, "invalid_request_token")
        self.assertFalse(invalid_pages)
        
        valid_pages = self.social_center.get_pages(self.TEST_PAGED_SITE, self.test_paged_bot._valid_main_token)
        self.assertTrue(valid_pages)
        self.assertEqual(len(valid_pages), 10)
        for i in range(10):
            page = valid_pages[i]
            self.assertEqual(page["id"], str(i+1))
            self.assertEqual(page["name"], "Page " + str(i+1))
    
    def test_social_bot_can_logout(self):
        self.social_center.logout(self.TEST_SITE)
        
        self.assertFalse(self.social_center.is_logged_in(self.TEST_SITE))
        self.assertFalse(hasattr(self.test_bot, "main_token"))
        self.assertFalse(hasattr(self.test_bot, "sub_token"))
    
    def test_social_bot_can_only_post_while_logged_in(self):
        title = "Test title"
        content = "Test content"
        link = "Test link"
    
        self.assertFalse(self.social_center.is_logged_in(self.TEST_SITE))
        
        logged_out_valid_results = self.social_center.publish(title, content, link)
        logged_out_invalid_results = self.social_center.publish(None, None, None)
        self.assertFalse(logged_out_valid_results)
        self.assertFalse(logged_out_invalid_results)
        
        self.social_center.authenticate(self.TEST_SITE, "main_token", "sub_token")
        #import pdb; pdb.set_trace()
        logged_in_valid_results = self.social_center.publish(title, content, link)
        logged_in_invalid_results = self.social_center.publish(None, None, None)
        self.assertTrue(logged_in_valid_results)
        self.assertTrue(logged_in_invalid_results)
        
        valid_result = logged_in_valid_results[0]
        self.assertEqual(valid_result["site"], self.TEST_SITE)
        self.assertNotIn("error", valid_result)
        self.assertIn("result", valid_result)
        self.assertEqual(valid_result["result"]["title"], title)
        self.assertEqual(valid_result["result"]["content"], content)
        self.assertEqual(valid_result["result"]["link"], link)
        
        invalid_result = logged_in_invalid_results[0]
        self.assertEqual(invalid_result["site"], self.TEST_SITE)
        self.assertIn("result", invalid_result)
        self.assertIn("error", invalid_result["result"])

class URLTest(TestCase):
    
    @staticmethod
    def generate_random_string(size, chars):
        return ''.join(random.choice(chars) for _ in range(size))

    # Ensure multiple alphanumeric URLs reach the same function
    def assert_dynamic_url_resolves_to(self, dynamic_url, view_func):
        for _ in range(10):
            site_name = self.generate_random_string(10, string.ascii_letters + string.digits)
            found = resolve(dynamic_url % site_name)
            self.assertEqual(found.func, view_func)
    
    def test_social_url_resolves_to_social_view(self):
        found = resolve("/social/")
        self.assertEqual(found.func, sn_views.social)
    
    def test_social_test_url_resolves_to_social_test_view(self):
        found = resolve("/social/test")
        self.assertEqual(found.func, sn_views.social_test)
    
    def test_social_post_url_resolves_to_social_post_view(self):
        found = resolve("/social/post")
        self.assertEqual(found.func, sn_views.social_post)
    
    def test_logout_url_resolves_to_logout_view(self):
        self.assert_dynamic_url_resolves_to("/social/%s/logout", sn_views.social_logout)
    
    def test_auth_url_resolves_to_auth_view(self):
        self.assert_dynamic_url_resolves_to("/social/%s/auth", sn_views.social_auth)
    
    def test_callback_url_resolves_to_callback_view(self):
        self.assert_dynamic_url_resolves_to("/social/%s/callback", sn_views.social_callback)
    
    def test_page_select_url_resolves_to_page_select_view(self):
        self.assert_dynamic_url_resolves_to("/social/%s/page", sn_views.social_page_select)

class ViewLogicTest(TestCase):

    TEST_SITE = "test"
    TEST_PAGED_SITE = "test_paged"
    
    @staticmethod
    def generate_get_request():
        get_request = HttpRequest()
        get_request.method = "GET"
        get_request.session = {}
        get_request.META["SERVER_NAME"] = "testapp.com"
        get_request.META["SERVER_PORT"] = "12345"
        
        return get_request
    
    @classmethod
    def setUpClass(self):
        self.test_bot = TestBot()
        self.test_paged_bot = TestBotWithPages()
        self.social_center = SocialCenter()
        self.default_site_info = self.social_center.get_sites()
        self.social_center.add_site(self.TEST_SITE, self.test_bot)
        self.social_center.add_site(self.TEST_PAGED_SITE, self.test_paged_bot)
    
    @classmethod
    def tearDownClass(self):
        self.social_center.logout(self.TEST_SITE)
        self.social_center.logout(self.TEST_PAGED_SITE)
        
        self.social_center.remove_site(self.TEST_SITE)
        self.social_center.remove_site(self.TEST_PAGED_SITE)
        
        del self.social_center
        del self.test_bot
        del self.test_paged_bot
    
    def test_social_view_has_correct_elements(self):
        sites = self.social_center.get_sites()
        for site_id, site in sites.items():
            site["auth_uri"] = "/social/%s/auth" % site_id
        expected_html = render_to_string("socialnetwork-main.html", { "sites" : sites })
        
        request = self.generate_get_request()
        request.method = "POST"
        invalid_response = sn_views.social(request)
        request.method = "GET"
        valid_response = sn_views.social(request)
        
        self.assertNotEqual(invalid_response.content.decode(), expected_html)
        self.assertEqual(valid_response.content.decode(), expected_html)
        
        # Test view changes after one site has been authenticated
        self.social_center.authenticate(self.TEST_SITE, "main_token", "sub_token")
        updated_sites = self.social_center.get_sites()
        for site_id, site in updated_sites.items():
            site["auth_uri"] = "/social/%s/auth" % site_id
        updated_sites[self.TEST_SITE]["logout_uri"] = "/social/%s/logout" % self.TEST_SITE
        
        request.method = "GET"
        updated_valid_response = sn_views.social(request)
        updated_expected_html = render_to_string("socialnetwork-main.html", { "sites" : updated_sites })
        self.social_center.logout(self.TEST_SITE)
        self.assertEqual(updated_valid_response.content.decode(), updated_expected_html)
    
    def test_social_test_view_has_correct_elements(self):
        expected_html = render_to_string("socialnetwork-post-test.html", { "social_post_uri" : "/social/post" })
        
        request = HttpRequest()
        request.method = "POST"
        invalid_response = sn_views.social_test(request)
        request.method = "GET"
        valid_response = sn_views.social_test(request)
        
        self.assertNotEqual(invalid_response.content.decode(), expected_html)
        self.assertEqual(valid_response.content.decode(), expected_html)
    
    def test_social_auth_view_has_correct_elements(self):
        get_request = self.generate_get_request()
        
        not_found_response = sn_views.social_auth(get_request, "non_existant_site")
        self.assertEqual(not_found_response.status_code, 404)
        
        self.social_center.authenticate(self.TEST_SITE, "main_token", "sub_token")
        already_logged_in_response = sn_views.social_auth(get_request, self.TEST_SITE)
        self.assertEqual(already_logged_in_response.status_code, 302)
        self.assertEqual(already_logged_in_response.url, "/social/")
        
        self.social_center.logout(self.TEST_SITE)
        test_auth_data_key = "%s_auth_data" % self.TEST_SITE
        callback_url = get_request.build_absolute_uri("/social/%s/callback" % self.TEST_SITE)
        oauth_url, auth_data = self.social_center.start_authentication(self.TEST_SITE, callback_url)
        
        auth_response = sn_views.social_auth(get_request, self.TEST_SITE)
        self.assertIn(test_auth_data_key, get_request.session)
        self.assertEqual(get_request.session[test_auth_data_key], auth_data)
        self.assertEqual(auth_response.status_code, 302)
        self.assertEqual(auth_response.url, oauth_url)
    
    def test_social_callback_view_has_correct_elements(self):
        get_request = self.generate_get_request()
        
        not_found_response = sn_views.social_callback(get_request, "non_existant_site")
        self.assertEqual(not_found_response.status_code, 404)
        
        self.assertRaises(BaseException, sn_views.social_callback, get_request, self.TEST_SITE)
        self.assertRaises(BaseException, sn_views.social_callback, get_request, self.TEST_PAGED_SITE)
        
        test_client_token_name = self.test_bot.get_client_token_name()
        test_paged_client_token_name = self.test_paged_bot.get_client_token_name()
        test_auth_data_key = "%s_auth_data" % self.TEST_SITE
        test_paged_auth_data_key = "%s_auth_data" % self.TEST_PAGED_SITE
        
        test_auth_data = self.test_bot.start_authentication("http://testapp.com/")[1]
        test_paged_auth_data = self.test_paged_bot.start_authentication("http://testapp.com/")[1]
        
        test_request = copy.deepcopy(get_request)
        
        test_request.session = { test_auth_data_key : test_auth_data}
        test_request.GET[test_client_token_name] = "invalid_code"
        test_invalid_code_response = sn_views.social_callback(test_request, self.TEST_SITE)
        self.assertEqual(test_invalid_code_response.status_code, 500)
        
        test_request.session = { test_auth_data_key : test_auth_data}
        test_request.GET[test_client_token_name] = "valid_code"
        test_valid_code_response = sn_views.social_callback(test_request, self.TEST_SITE)
        self.assertEqual(test_valid_code_response.status_code, 302)
        self.assertEqual(test_valid_code_response.url, "/social/")
        
        test_paged_request = copy.deepcopy(get_request)
        
        test_paged_request.session = { test_paged_auth_data_key : test_paged_auth_data}
        test_paged_request.GET[test_paged_client_token_name] = self.test_paged_bot._valid_client_token
        test_paged_valid_code_response = sn_views.social_callback(test_paged_request, self.TEST_PAGED_SITE)
        
        pages = self.social_center.get_pages(self.TEST_PAGED_SITE, self.test_paged_bot._valid_main_token)
        expected_html = render_to_string("socialnetwork-select-page.html", {
                "pages" : pages,
                "root_uri" : "/social/",
                "process_uri" : "/social/%s/page" % self.TEST_PAGED_SITE
            })
        
        self.assertEqual(test_paged_valid_code_response.content.decode(), expected_html)