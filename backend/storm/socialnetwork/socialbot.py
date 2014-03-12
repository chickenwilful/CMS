from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
import json

import facebook
from twython import Twython, TwythonError, TwythonRateLimitError, TwythonAuthError
from requests_oauthlib import OAuth2Session
import requests

class SocialBot(object):
    """Abstract class definition for all SocialBots.
    
    A SocialBot is able to provide authentication and post publishing services
    to the containing SocialCenter.
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def post(self, title, content, link):
        """Posts content to the site managed by the SocialBot
        
        Publishes content to the website. All arguments are required.
        
        @type title: str
        @type content: str
        @type link: str
        
        @param title: The title of the post.
        @param content: A string containing the main body of the post.
        @param link: A link to a related resource
        
        @rtype: dict
        @return:
            A dict containing all the returned data from the website. If an
            error is returned, the dict will contain the "error" key, e.g.:
            
            {
             ...
             "error" : "Unable to publish to website!",
             ...
            }
        """
        pass
    
    @abstractmethod
    def authenticate(self, token, sub_token=None):
        """Authenticates the SocialBot with the given token(s).
        
        @type token: str
        @type sub_token: str
        
        @param token: The main token used by the SocialBot for requests.
        @param sub_token: The second token. May or may not be required by the
                          implemented SocialBot.
        
        @rtype: dict
        @return: A dict containing the main and sub tokens. For example:
            {"main_token": "fQ@)NG#fa-f",
             "sub_token": "43295t2-2"}
        """
        pass
        
    @abstractmethod
    def refresh_token(self):
        """Refreshes the token(s) held by the SocialBot.
        
        Some websites provide access tokens that expire after some time. The
        implementing SocialBot may provide a method to refresh the token.
        
        @rtype: dict
        @return: A dict containing the main and sub tokens. For example:
            {"main_token": "fQ@)NG#fa-f",
             "sub_token": "43295t2-2"}
        """
        pass
    
    @abstractmethod
    def start_authentication(self, callback_url):
        """Begins the user-based OAuth authentication process.
        
        @type  callback_url: str
        @param callback_url: A URL to a suitable endpoint which can process the
                             response from the website.
        
        @rtype: tuple
        @return: A tuple containing the OAuth authorization URL, and a dict
                 containing additional tokens to be stored in the session.
        """
        pass
    
    @abstractmethod
    def process_token(self, client_token, **kwargs):
        """Processes the returned token from the OAuth authentication process.
        
        Note that this function can take in any number of keyword arguments,
        and will typically take in the same arguments as the tokens returned
        by C{start_authentication}.
        
        @type  client_token: str
        @param client_token: The token returned from the website.
        
        @keyword client_secret: The secret key for a registered app on the
            website, which may be required for the token exchange.
        @keyword callback_url: The callback URL specified in the beginning
            of the OAuth process, in C{start_authentication}. May be required
            by the website (and the SocialBot).
        
        @rtype: dict
        @return: A dict containing the main token, as well as any other token
            returned by the website.
        """
        pass
    
    @abstractmethod
    def get_pages(self, request_token):
        """Retrieves all pages hosted by the authenticated user..
        
        @type  request_token: str
        @param request_token: The token used for requests to the website.
        
        @rtype: list
        @return: A list of dicts containing page information. For example:
            [
                {"id": "3415", "name": "A Page",
                 "id": "326662", "name": "Another Page"},
                ...
            ]
        """
        pass
    
    @abstractmethod
    def clear_token(self):
        """Clears all tokens stored by the SocialBot
        """
        pass

class DummyBot(SocialBot):

    def process_token(self, client_token, **kwargs):
        pass

class FacebookBot(SocialBot):
    """A SocialBot that can interface with the Facebook Graph API.
    """

    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret
    
    def post(self, title, content, link):
        message = title + '\n\n' + content
        graph = facebook.GraphAPI(self._main_token)
        try:
            result = graph.put_object("me", "feed", message=message, link=link, name=title) 
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
    """A SocialBot that can interface with the Twitter REST API.
    """

    @staticmethod
    def __get_char_limit():
        return 140

    @staticmethod
    def __get_url_length():
        return 23

    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret
    
    def post(self, title, content, link):
        twitter = Twython(self.__app_id, self.__app_secret,
                          self._main_token, self._sub_token)
        
        char_limit = self.__get_char_limit() - self.__get_url_length() - 1
        
        status_text = title
        if len(title) > char_limit:
            status_text = title[:(char_limit-3)] + "..."
        
        try:
            result = twitter.update_status(status=status_text + " " + link)
        except TwythonRateLimitError as e:
            return { "error" : e.msg }
        except TwythonAuthError as e:
            return { "error" : e.msg }
        except TwythonError as e:
            return { "error" : e.msg }
        return result
    
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
    """A SocialBot that can interface with the Google+ Page API.
    """

    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret

    @staticmethod
    def __get_token_dict(access_token):
        """Generates a token valid for use with OAuth2Sessions
        
        @type  access_token: str
        @param access_token: The access token string for the session.
        
        @rtype: dict
        @return: A dict containing both the access token, and the required
                 token_type as follows:
                 {"access_token": 'anf@_(QRNF2',
                 "token_type": "Bearer"}
        """
        return { "access_token" : access_token, "token_type" : "Bearer" }
    
    @staticmethod
    def __missing_token_type_compliance_hook(response):
        """OAuthlib compliance hook for Buffer
        
        Buffer does not return a token_type with its access token, so we must
        insert the token_type into the response.
        
        @type  response: HttpResponse
        @param response: Response retrieved from the server.
        
        @rtype: HttpResponse
        @return: The same response but modified to fit the OAuth specification.
        """
        token = json.loads(response.text)
        token['token_type'] = 'Bearer'
        response._content = json.dumps(token).encode('UTF-8')
        return response
    
    def post(self, title, content, link):
        message = title + '\n\n' + content
        
        token_dict = self.__get_token_dict(self._main_token)
        profile_id = self._sub_token
        
        post_data = {}
        post_data["text"] = message
        post_data["profile_ids[]"] = profile_id
        post_data["now"] = True
        post_data["media[title]"] = title
        post_data["media[link]"] = link
        
        oauth_session = OAuth2Session(self.__app_id, token=token_dict)
        response = oauth_session.post("https://api.bufferapp.com/1/updates/create.json", data=post_data)
        response_json = response.json()
        
        result = {}
        if not response_json["success"]:
            result = response_json
            result["error"] = "Unable to post to Google+."
        else:
            result = response_json["updates"][0]
            if result["status"] != "sent":
                result["error"] = "Unable to post to Google+."
        
        return result
    
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
        auth_data = {}
        
        oauth_session = OAuth2Session(self.__app_id, redirect_uri=callback_url)
        oauth_url, state = oauth_session.authorization_url('https://bufferapp.com/oauth2/authorize')
        
        auth_data["state"] = state
        
        return oauth_url, auth_data

    def process_token(self, client_token, **kwargs):
        callback_url = kwargs.get("callback_url")
        
        oauth_session = OAuth2Session(self.__app_id, redirect_uri=callback_url)
        # Register the Buffer compliance hook
        oauth_session.register_compliance_hook("access_token_response",
                                               self.__missing_token_type_compliance_hook)
        token = oauth_session.fetch_token("https://api.bufferapp.com/1/oauth2/token.json",
                                          code=client_token,
                                          client_secret=self.__app_secret)
        
        result = {}
        if "access_token" in token:
            result["main_token"] = token["access_token"]
        else:
            result["error"] = "Unable to retrieve access token."
        
        return result

    def get_pages(self, request_token):
        request_token_dict = self.__get_token_dict(request_token)
        
        oauth_session = OAuth2Session(self.__app_id, token=request_token_dict)
        response = oauth_session.get("https://api.bufferapp.com/1/profiles.json")
        
        profiles = response.json()
        pages = []
        for profile in profiles:
            if profile["service"] == "google" and profile["service_type"] == "page":
                page = {}
                page["id"] = profile["id"]
                page["name"] = profile["formatted_username"]
                pages.append(page)
        
        return pages
    
    def clear_token(self):
        if hasattr(self, "_main_token"):
            del self._main_token
        if hasattr(self, "_sub_token"):
            del self._sub_token