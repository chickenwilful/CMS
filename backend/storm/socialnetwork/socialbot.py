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
    def set_token(self, token, sub_token=None):
        pass
        
    @abstractmethod
    def refresh_token(self):
        pass
    
    @abstractmethod
    def process_token(self, client_token, **kwargs):
        pass
    
    @abstractmethod
    def clear_token(self):
        pass

class DummyBot(SocialBot):

    def process_token(self, client_token, **kwargs):
        pass

class FacebookBot(SocialBot):

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
    
    def post(self, title, content, link):
        message = title + '\n\n' + content
        graph = facebook.GraphAPI(self.main_token)
        try:
            result = graph.put_object("me", "feed", message=message, link=link, name=title, description=content) 
        except facebook.GraphAPIError as e:
            return { "error" : e.message }
        return result
    
    def set_token(self, token, sub_token=None):
        self.main_token = token
        
    def refresh_token(self):
        # Facebook Page access tokens last forever
        pass

    def process_token(self, client_token, **kwargs):
        page_id = kwargs.get("page_id")
        graph = facebook.GraphAPI(client_token, kwargs.get("expires", None))
        extension_response = graph.extend_access_token(self.app_id, self.app_secret)
        # Recreate Graph API object with new credentials
        extended_token = extension_response.get("access_token")
        graph = facebook.GraphAPI(extended_token)
        
        result = {}
        pages = graph.get_object("me/accounts").get("data", None)
        
        if pages:
            displayed_pages = []
            for page in pages:
                if page["id"] == page_id:
                    result["main_token"] = page["access_token"]
                    self.main_token = page["access_token"]
        
        if "main_token" not in result:
            result["error"] = "Page not found."
        
        return result
    
    def clear_token(self):
        if hasattr(self, "main_token"):
            del self.main_token

class TwitterBot(SocialBot):

    @staticmethod
    def get_char_limit():
        return 140

    @staticmethod
    def get_url_length():
        return 23

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
    
    def post(self, title, content, link):
        twitter = Twython(self.app_id, self.app_secret,
                          self.main_token, self.sub_token)
        
        char_limit = self.get_char_limit() - self.get_url_length() - 1
        
        status_text = title
        if len(title) > char_limit:
            status_text = title[:(char_limit-3)] + "..."
        
        return twitter.update_status(status=status_text + " " + link)
    
    def set_token(self, token, sub_token=None):
        self.main_token = token
        if sub_token:
            self.sub_token = sub_token
        
    def refresh_token(self):
        # Twitter access tokens last forever
        pass

    def process_token(self, client_token, **kwargs):
        twitter_oauth_token = kwargs["oauth_token"]
        twitter_oauth_secret = kwargs["oauth_secret"]
        twitter = Twython(self.app_id, self.app_secret,
                          twitter_oauth_token, twitter_oauth_secret)
        
        authorized_tokens = twitter.get_authorized_tokens(client_token)
        
        result = {}
        
        if "oauth_token" in authorized_tokens:
            self.main_token = authorized_tokens["oauth_token"]
            self.sub_token = authorized_tokens["oauth_token_secret"]
            result["main_token"] = authorized_tokens["oauth_token"]
            result["sub_token"] = authorized_tokens["oauth_token_secret"]
        else:
            result["error"] = "Unable to retrieve tokens."
        
        return result
    
    def clear_token(self):
        if hasattr(self, "main_token"):
            del self.main_token
        if hasattr(self, "sub_token"):
            del self.sub_token

# Even though this bot is meant to post updates to G+, it will post them to the Buffer API instead.
# Google has yet to release an API for Pages publicly, so we have to do it from a 3rd party API.
class GPlusBot(SocialBot):

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
    
    def post(self, title, content, link):
        pass
    
    def set_token(self, token, sub_token=None):
            self.main_token = token
            if sub_token:
                self.sub_token = sub_token
        
    def refresh_token(self):
        # No known method of refreshing a Buffer token
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
    
    def clear_token(self):
        if hasattr(self, "main_token"):
            del self.main_token
        if hasattr(self, "sub_token"):
            del self.sub_token