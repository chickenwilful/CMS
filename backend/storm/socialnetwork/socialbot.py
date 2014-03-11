from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

import facebook
from twython import Twython
from requests_oauthlib import OAuth2Session
import requests

class SocialBot(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def post(self, title, content, link):
        pass
    
    @abstractmethod
    def authenticate(self, token, sub_token=None):
        pass
        
    @abstractmethod
    def refresh_token(self):
        pass
    
    @abstractmethod
    def start_authentication(self, callback_url):
        pass
    
    @abstractmethod
    def process_token(self, client_token, **kwargs):
        pass
    
    @abstractmethod
    def get_pages(self, request_token):
        pass
    
    @abstractmethod
    def clear_token(self):
        pass

class DummyBot(SocialBot):

    def process_token(self, client_token, **kwargs):
        pass

class FacebookBot(SocialBot):

    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret
    
    def post(self, title, content, link):
        message = title + '\n\n' + content
        graph = facebook.GraphAPI(self.__main_token)
        try:
            result = graph.put_object("me", "feed", message=message, link=link, name=title, description=content) 
        except facebook.GraphAPIError as e:
            return { "error" : e.message }
        return result
    
    def authenticate(self, token, sub_token=None):
        result = {}
            
        if sub_token:
            page_id = sub_token
            graph = facebook.GraphAPI(token)
            
            pages = graph.get_object("me/accounts").get("data", None)
            
            for page in pages:
                if page["id"] == page_id:
                    self._main_token = page["access_token"]
        else:
            self._main_token = token
        
        if hasattr(self, "_main_token"):
            result["main_token"] = self._main_token
        
        return result
        
    def refresh_token(self):
        # Facebook Page access tokens last forever
        pass
    
    def start_authentication(self, callback_url):
        # Authentication is handled by the Facebook Javascript SDK
        pass

    def process_token(self, client_token, **kwargs):
        if isinstance(client_token, dict):
            user = facebook.get_user_from_cookie(client_token, self.__app_id, self.__app_secret)
            client_token = user["access_token"]
        
        graph = facebook.GraphAPI(client_token)
        extension_response = graph.extend_access_token(self.__app_id, self.__app_secret)
        
        extended_token = extension_response.get("access_token")
        
        result = {}
        result["main_token"] = extended_token
        
        if "main_token" not in result:
            result["error"] = "Page not found."
        
        return result
    
    def get_pages(self, request_token):
        graph = facebook.GraphAPI(request_token)
        retrieved_pages = graph.get_object("me/accounts").get("data", None)
        pages = []
        
        if retrieved_pages:
            for retrieved_page in retrieved_pages:
                page = {
                    "id" : retrieved_page["id"],
                    "name" : retrieved_page["name"]
                }
                pages.append(page)
        
        return pages
    
    def clear_token(self):
        if hasattr(self, "_main_token"):
            del self._main_token

class TwitterBot(SocialBot):

    @staticmethod
    def get_char_limit():
        return 140

    @staticmethod
    def get_url_length():
        return 23

    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret
    
    def post(self, title, content, link):
        twitter = Twython(self.__app_id, self.__app_secret,
                          self._main_token, self._sub_token)
        
        char_limit = self.get_char_limit() - self.get_url_length() - 1
        
        status_text = title
        if len(title) > char_limit:
            status_text = title[:(char_limit-3)] + "..."
        
        return twitter.update_status(status=status_text + " " + link)
    
    def authenticate(self, token, sub_token=None):
        if not sub_token:
            raise ValueError("Twitter requires the OAuth secret as a sub token")
        self._main_token = token
        self._sub_token = sub_token
        
        result = {}
        result["main_token"] = token
        result["sub_token"] = sub_token
        
        return result
        
    def refresh_token(self):
        # Twitter access tokens last forever
        pass
    
    def start_authentication(self, callback_url):
        auth_data = {}
        
        twitter = Twython(self.__app_id, self.__app_secret)
        auth = twitter.get_authentication_tokens(callback_url=callback_url)
        
        auth_data["twitter_oauth_token"] = auth["oauth_token"]
        auth_data["twitter_oauth_token_secret"] = auth["oauth_token_secret"]
        oauth_url = auth["auth_url"]
        
        return oauth_url, auth_data

    def process_token(self, client_token, **kwargs):
        twitter_oauth_token = kwargs["oauth_token"]
        twitter_oauth_secret = kwargs["oauth_secret"]
        twitter = Twython(self.__app_id, self.__app_secret,
                          twitter_oauth_token, twitter_oauth_secret)
        
        authorized_tokens = twitter.get_authorized_tokens(client_token)
        
        result = {}
        
        if "oauth_token" in authorized_tokens:
            result["main_token"] = authorized_tokens["oauth_token"]
            result["sub_token"] = authorized_tokens["oauth_token_secret"]
        else:
            result["error"] = "Unable to retrieve tokens."
        
        return result

    def get_pages(self, request_token):
        return None
        
    def clear_token(self):
        if hasattr(self, "_main_token"):
            del self._main_token
        if hasattr(self, "_sub_token"):
            del self._sub_token

# Even though this bot is meant to post updates to G+, it will post them to the Buffer API instead.
# Google has yet to release an API for Pages publicly, so we have to do it from a 3rd party API.
class GPlusBot(SocialBot):

    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret
    
    def post(self, title, content, link):
        pass
    
    def authenticate(self, token, sub_token=None):
        if not sub_token:
            raise ValueError("Google+ requires the profile ID as a sub token")
        self._main_token = token        
        self._sub_token = sub_token
        
        result = {}
        result["main_token"] = token
        result["sub_token"] = sub_token
        
        return result
        
    def refresh_token(self):
        # No known method of refreshing a Buffer token
        pass
    
    def start_authentication(self, callback_url):
        #TODO: implement OAuth
        pass

    def process_token(self, client_token, **kwargs):
        callback_url = kwargs.get("callback_url")
        
        # We use the requests API instead of OAuth to retrieve the access token
        # Buffer does not follow specification and return token_type as expected
        
        post_data = {
            "client_id" : self.app_id,
            "client_secret" : self.app_secret,
            "redirect_uri" : callback_url,
            "code" : client_token,
            "grant_type" : "authorization_code"
        }
        
        response = requests.post("https://api.bufferapp.com/1/oauth2/token.json", data=post_data).json()
        result = {}
        if "access_token" in response:
            result["main_token"] = response["access_token"]
        else:
            result["error"] = "Unable to retrieve access token."
        
        return result

    def get_pages(self, request_token):
        #TODO: Retrieve Buffer profiles related to Google+
        return None
    
    def clear_token(self):
        if hasattr(self, "_main_token"):
            del self._main_token
        if hasattr(self, "_sub_token"):
            del self._sub_token