from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
import facebook

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

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
    
    def post(self, title, content, link):
        return None
    
    def set_token(self, token, sub_token=None):
        self.main_token = token
        if sub_token:
            self.sub_toke = sub_token
        
    def refresh_token(self):
        # Facebook Page access tokens last forever
        pass

    def process_token(self, client_token, **kwargs):
        return None
    
    def clear_token(self):
        if hasattr(self, "main_token"):
            del self.main_token
        if hasattr(self, "sub_token"):
            del self.sub_token