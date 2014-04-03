from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from urlparse import urlparse
import json

import facebook
from twython import Twython, TwythonError, TwythonRateLimitError, TwythonAuthError
from requests_oauthlib import OAuth1Session, OAuth2Session
import requests


class SocialBot(object):
    """Abstract class definition for all SocialBots.
    
    A SocialBot is able to provide authentication and post publishing services
    to the containing SocialCenter.
    """
    __metaclass__ = ABCMeta

    @staticmethod
    def _get_token_dict(access_token):
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
    
    @abstractmethod
    def must_refresh_token(self):
        """Whether the SocialBot needs its tokens refreshed every so often.
        
        @rtype: bool
        @return: True if the tokens need to be refreshed.
        """
        pass
    
    @abstractmethod
    def must_select_page(self):
        """Whether the SocialBot requires that a page be selected.
        
        @rtype: bool
        @return: True if a page needs to be selected.
        """
        pass
    
    @abstractmethod
    def get_site_name(self):
        """The site name represented by the SocialBot.
        
        @rtype: str
        @return: The full name of the site represented.
        """
        pass
    
    @abstractmethod
    def get_client_token_name(self):
        """The client token name returned in the OAuth callback.
        
        OAuth services return an authorization code in the callback from their
        login page, but the name of this code differs among different services.
        This name will be one of the keys in the GET request of the callback,
        if the user authorization was successful.
        
        @rtype: str
        @return: The name of the authorization code.
        """
        pass
    
    @abstractmethod
    def get_account_name(self):
        """The account/page name on which the SocialBot is publishing posts on.
        
        @rtype: str
        @return: The SocialBot will publish posts on the name returned by this
                 method. If the SocialBot does not allow selection of pages,
                 this will be the account name. Otherwise, this will be a page
                 name.
        """
        pass
    
    @abstractmethod
    def get_account_url(self):
        """The account/page URL on which the SocialBot is publishing posts on.
        
        @rtype: str
        @return: The SocialBot will publish posts on the URL returned by this
                 method. If the SocialBot does not allow selection of pages,
                 this will be the account URL. Otherwise, this will be a page
                 URL.
        """
        pass
    
    @abstractmethod
    def post(self, title, content, link):
        """Posts content to the site managed by the SocialBot
        
        Publishes content to the website. The content to be posted cannot be
        empty, i.e. either title or content must not be left blank.
        
        @type title: str
        @type content: str
        @type link: str
        
        @param title: The title of the post.
        @param content: The main body of the post.
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
    def process_token(self, client_token, auth_data):
        """Processes the returned token from the OAuth authentication process.
        
        Note that this function can take in any number of keyword arguments,
        and will typically take in the same arguments as the tokens returned
        by C{start_authentication}.
        
        The returned token may be used in C{authenticate} immediately, or be
        used in more refined requests first.
        
        @type  client_token: str
        @type auth_data: dict
        
        @param client_token: The token returned from the website.
        @param auth_data: All the session authentication information returned
                          by C{start_authentication}.
        
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
    
    __site_name = "Facebook"
    __client_token_name = "code"
    __permissions = ["manage_pages","status_update"]

    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret
    
    def __retrieve_account_details(self):
        graph = facebook.GraphAPI(self._main_token)
        #import pdb; pdb.set_trace()
        try:
            page_info = graph.get_object("me")
        except facebook.GraphAPIError as e:
            return None, None
        
        if "name" in page_info:
            page_name = page_info["name"]
            page_url = page_info["link"]
            self._page_name = page_name
            self._page_url = page_url
            return page_name, page_url
        else:
            return None, None
    
    def must_refresh_token(self):
        return False
    
    def must_select_page(self):
        return True
    
    def get_site_name(self):
        return self.__site_name
    
    def get_client_token_name(self):
        return self.__client_token_name
    
    def get_account_name(self):
        if hasattr(self, "_page_name"):
            return self._page_name
        elif hasattr(self, "_main_token"):
            page_name, page_url = self.__retrieve_account_details()
            if page_name:
                return page_name
            else:
                return "Unknown"
        return "Unauthorized"
    
    def get_account_url(self):
        if hasattr(self, "_page_url"):
            return self._page_url
        elif hasattr(self, "_main_token"):
            page_name, page_url = self.__retrieve_account_details()
            return page_url
        return None
    
    def post(self, title, content, link):
        message = title or content or None
        if not message:
            return {"error" : "No content in post."}
        if title and content:
            message += "\n\n" + content
        
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
        auth_data = {}
        auth_data["callback_url"] = callback_url
        
        oauth_url = facebook.auth_url(self.__app_id, callback_url,
                                      perms = self.__permissions)
        
        return oauth_url, auth_data

    def process_token(self, client_token, auth_data):
        callback_url = auth_data["callback_url"]
        
        auth_response = facebook.get_access_token_from_code(client_token,
                                                           callback_url,
                                                           self.__app_id,
                                                           self.__app_secret)
        
        if "access_token" not in auth_response:
            return { "error" : "Unable to authenticate code." }
        
        access_token = auth_response["access_token"]
        
        graph = facebook.GraphAPI(access_token)
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
        if hasattr(self, "_page_name"):
            del self._page_name
        if hasattr(self, "_page_url"):
            del self._page_url

class TwitterBot(SocialBot):
    """A SocialBot that can interface with the Twitter REST API.
    """
    
    __site_name = "Twitter"
    __client_token_name = "oauth_verifier"
    __base_account_url = "https://twitter.com/%s"

    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret

    @staticmethod
    def __get_char_limit():
        return 140

    @staticmethod
    def __get_url_length():
        return 23
    
    def __retrieve_account_details(self):
        twitter = Twython(self.__app_id, self.__app_secret,
                          self._main_token, self._sub_token)
        
        try:
            user_info = twitter.verify_credentials()
        except TwythonAuthError as e:
            return None, None
        
        if "screen_name" in user_info:
            account_name = user_info["screen_name"]
            account_url = self.__base_account_url % account_name
            self._account_name = account_name
            self._account_url = account_url
            return account_name, account_url
        else:
            return None, None
    
    def must_refresh_token(self):
        return False
    
    def must_select_page(self):
        return False
    
    def get_site_name(self):
        return self.__site_name
    
    def get_client_token_name(self):
        return self.__client_token_name
    
    def get_account_name(self):
        if hasattr(self, "_account_name"):
            return self._account_name
        elif hasattr(self, "_main_token"):
            username, account_url = self.__retrieve_account_details()
            
            if username:
                return username
            else:
                return "Unknown"
        return "Unauthorized"
    
    def get_account_url(self):
        if hasattr(self, "_account_url"):
            return self._account_url
        elif hasattr(self, "_main_token"):
            page_name, account_url = self.__retrieve_account_details()
            return account_url
        return None
    
    def post(self, title, content, link):
        status_text = title or content or None
        if not status_text:
            return {"error" : "No content in post."}
            
        twitter = Twython(self.__app_id, self.__app_secret,
                          self._main_token, self._sub_token)
        
        char_limit = self.__get_char_limit() - self.__get_url_length() - 1
        
        if len(status_text) > char_limit:
            status_text = status_text[:(char_limit-3)] + "..."
        
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
        
        auth_data["oauth_token"] = auth["oauth_token"]
        auth_data["oauth_token_secret"] = auth["oauth_token_secret"]
        oauth_url = auth["auth_url"]
        
        return oauth_url, auth_data

    def process_token(self, client_token, auth_data):
        twitter_oauth_token = auth_data["oauth_token"]
        twitter_oauth_secret = auth_data["oauth_token_secret"]
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
        raise NotImplementedError("This SocialBot has no pages.")
        
    def clear_token(self):
        if hasattr(self, "_main_token"):
            del self._main_token
        if hasattr(self, "_sub_token"):
            del self._sub_token
        if hasattr(self, "_account_name"):
            del self._account_name
        if hasattr(self, "_account_url"):
            del self._account_url

# Even though this bot is meant to post updates to G+, it will post them to the Buffer API instead.
# Google has yet to release an API for Pages publicly, so we have to do it from a 3rd party API.
class GPlusBot(SocialBot):
    """A SocialBot that can interface with the Google+ Page API.
    """
    
    __site_name = "Google+"
    __client_token_name = "code"
    __authorize_url = "https://bufferapp.com/oauth2/authorize"
    __token_url = "https://api.bufferapp.com/1/oauth2/token.json"
    
    __post_url = "https://api.bufferapp.com/1/updates/create.json"
    __profiles_url = "https://api.bufferapp.com/1/profiles.json"
    __profile_info_url = "https://api.bufferapp.com/1/profiles/%s.json"
    __base_page_url = "https://plus.google.com/%s/"

    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret
    
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
    
    def __create_oauth_session(self, token=None):
        token = token or self._main_token
        token_dict = self._get_token_dict(token)
        return OAuth2Session(self.__app_id, token=token_dict)
    
    def __retrieve_account_details(self):
        page_id = self._sub_token
        oauth_session = self.__create_oauth_session()
        
        page_info = oauth_session.get(self.__profile_info_url % page_id).json()
        if "formatted_username" in page_info:
            page_name = page_info["formatted_username"]
            
            page_url = self.__base_page_url % page_info["service_id"]
            self._page_name = page_name
            self._page_url = page_url
            return page_name, page_url
        else:
            return None, None
    
    def must_refresh_token(self):
        return False
    
    def must_select_page(self):
        return True
    
    def get_site_name(self):
        return self.__site_name
    
    def get_client_token_name(self):
        return self.__client_token_name
    
    def get_account_name(self):
        if hasattr(self, "_page_name"):
            return self._page_name
        elif hasattr(self, "_main_token"):
            page_name, page_url = self.__retrieve_account_details()
            
            if page_name:
                return page_name
            else:
                return "Unknown"
        return "Unauthorized"
    
    def get_account_url(self):
        if hasattr(self, "_page_url"):
            return self._page_url
        elif hasattr(self, "_main_token"):
            page_name, page_url = self.__retrieve_account_details()
            return page_url
        return None
    
    def post(self, title, content, link):
        message = title or content or None
        if not message:
            return {"error" : "No content in post."}
        if title and content:
            message += "\n\n" + content
        
        profile_id = self._sub_token
        
        post_data = {}
        post_data["text"] = message
        post_data["profile_ids[]"] = profile_id
        post_data["now"] = True
        post_data["media[title]"] = title
        post_data["media[link]"] = link
        
        oauth_session = self.__create_oauth_session()
        response = oauth_session.post(self.__post_url, data=post_data)
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
        oauth_url, state = oauth_session.authorization_url(self.__authorize_url)
        
        # auth_data["state"] = state
        auth_data["callback_url"] = callback_url
        
        return oauth_url, auth_data

    def process_token(self, client_token, auth_data):
        callback_url = auth_data["callback_url"]
        
        oauth_session = OAuth2Session(self.__app_id, redirect_uri=callback_url)
        # Register the Buffer compliance hook
        oauth_session.register_compliance_hook("access_token_response",
                                               self.__missing_token_type_compliance_hook)
        token = oauth_session.fetch_token(self.__token_url,
                                          code=client_token,
                                          client_secret=self.__app_secret)
        
        result = {}
        if "access_token" in token:
            result["main_token"] = token["access_token"]
        else:
            result["error"] = "Unable to retrieve access token."
        
        return result

    def get_pages(self, request_token):
        # import pdb; pdb.set_trace()
        oauth_session = self.__create_oauth_session(token=request_token)
        response = oauth_session.get(self.__profiles_url)
        
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
        if hasattr(self, "_page_name"):
            del self._page_name
        if hasattr(self, "_page_url"):
            del self._page_url

class TumblrBot(SocialBot):
    """A SocialBot that can interface with the Tumblr Blog API.
    """
    
    __site_name = "Tumblr"
    __client_token_name = "oauth_verifier"
    __request_token_url = "https://www.tumblr.com/oauth/request_token"
    __authorize_url = "https://www.tumblr.com/oauth/authorize"
    __access_token_url = "https://www.tumblr.com/oauth/access_token"
    
    __post_url = "https://api.tumblr.com/v2/blog/%s/post"
    __user_info_url = "https://api.tumblr.com/v2/user/info"
    __blog_info_url = "https://api.tumblr.com/v2/blog/%s/info"

    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret
    
    def __create_oauth_session(self, token=None, token_secret=None):
        token = token or self._main_token
        token_secret = token_secret or self._token_secret
        return OAuth1Session(self.__app_id,
                      client_secret=self.__app_secret,
                      resource_owner_key=token,
                      resource_owner_secret=token_secret)
    
    def __retrieve_account_details(self):
        hostname = self._sub_token
        params = { "api_key" : self.__app_id }
        
        response = requests.get(self.__blog_info_url % hostname, params=params)
        response_json = response.json()
        res_object = response_json["response"]
        
        if "blog" in res_object:
            blog = res_object["blog"]
            page_name = blog["title"]
            page_url = blog["url"]
            self._page_name = page_name
            self._page_url = page_url
            return page_name, page_url
        else:
            return None, None
    
    def must_refresh_token(self):
        return False
    
    def must_select_page(self):
        return True
    
    def get_site_name(self):
        return self.__site_name
    
    def get_client_token_name(self):
        return self.__client_token_name
    
    def get_account_name(self):
        if hasattr(self, "_page_name"):
            return self._page_name
        elif hasattr(self, "_main_token"):
            page_name, page_url = self.__retrieve_account_details()
            
            if page_name:
                return page_name
            else:
                return "Unknown"
        return "Unauthorized"
    
    def get_account_url(self):
        if hasattr(self, "_page_url"):
            return self._page_url
        elif hasattr(self, "_main_token"):
            page_name, page_url = self.__retrieve_account_details()
            return page_url
        return None
    
    def post(self, title, content, link):
        body = content or title or None
        if not body:
            return {"error" : "No content in post."}
        
        hostname = self._sub_token
        
        post_data = {}
        if link:
            post_data["type"] = "link"
            post_data["url"] = link
            if title:
                post_data["title"] = title
            if content:
                post_data["description"] = content
        else:
            post_data["type"] = "text"
            post_data["body"] = body
            if title:
                post_data["title"] = title
        
        oauth_session = self.__create_oauth_session()
        
        blog_post_url = self.__post_url % hostname
        response = oauth_session.post(blog_post_url, data=post_data)
        result = {}
        
        if response.status_code != 201:
            result["error"] = "Unable to post to %s." % self.__site_name
        
        return result
    
    def authenticate(self, token, sub_token=None):
        if not sub_token:
            raise ValueError("Tumblr requires the blog hostname as a sub token.")
        
        token_info = json.loads(token)
        
        self._main_token = token_info["oauth_token"]
        self._token_secret = token_info["oauth_token_secret"]
        self._sub_token = sub_token
        
        result = {}
        result["main_token"] = token
        result["sub_token"] = sub_token
        
        return result
        
    def refresh_token(self):
        # No known method of refreshing a Tumblr token
        pass
    
    def start_authentication(self, callback_url):
        auth_data = {}
        
        oauth_session = OAuth1Session(self.__app_id, client_secret=self.__app_secret)
        request_token_response = oauth_session.fetch_request_token(self.__request_token_url)
        
        oauth_token = request_token_response.get('oauth_token')
        oauth_token_secret = request_token_response.get('oauth_token_secret')
        
        if (oauth_token and oauth_token_secret) is None:
            return None, None
        
        oauth_url = oauth_session.authorization_url(self.__authorize_url)
        auth_data["oauth_token"] = oauth_token
        auth_data["oauth_token_secret"] = oauth_token_secret
        
        # auth_data["state"] = state
        # auth_data["callback_url"] = callback_url
        
        return oauth_url, auth_data

    def process_token(self, client_token, auth_data):
        oauth_session = OAuth1Session(self.__app_id,
                                      client_secret=self.__app_secret,
                                      resource_owner_key=auth_data["oauth_token"],
                                      resource_owner_secret=auth_data["oauth_token_secret"],
                                      verifier=client_token)
        token = oauth_session.fetch_access_token(self.__access_token_url)
        
        result = {}
        if "oauth_token" in token:
            result["main_token"] = json.dumps(token)
        else:
            result["error"] = "Unable to retrieve access token."
        
        return result

    def get_pages(self, request_token):
        oauth_tokens = json.loads(request_token)
        oauth_token = oauth_tokens["oauth_token"]
        oauth_token_secret = oauth_tokens["oauth_token_secret"]
        
        oauth_session = self.__create_oauth_session(token=oauth_token,
                                                    token_secret=oauth_token_secret)
        response = oauth_session.get(self.__user_info_url)
        
        response_object = response.json()["response"]
        user = response_object["user"]
        blogs = user["blogs"]
        pages = []
        for blog in blogs:
            page = {}
            hostname = urlparse(blog["url"]).hostname
            page["id"] = hostname
            page["name"] = blog["title"]
            pages.append(page)
        
        return pages
    
    def clear_token(self):
        if hasattr(self, "_main_token"):
            del self._main_token
        if hasattr(self, "_token_secret"):
            del self._token_secret
        if hasattr(self, "_sub_token"):
            del self._sub_token
        if hasattr(self, "_page_name"):
            del self._page_name
        if hasattr(self, "_page_url"):
            del self._page_url
