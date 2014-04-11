from django.conf import settings
from models import SocialToken
from datetime import datetime
from multiprocessing.pool import ThreadPool
import logging
import re

from socialbot import SocialBot, FacebookBot, TwitterBot, GPlusBot, TumblrBot

logger = logging.getLogger('storm')

class Singleton(type):
    """Singleton metaclass

    Any class that implements this metaclass will become a Singleton.
    All instances will actually point to the same instance of the class.

    Derived from: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SocialCenter(object):
    """Interface to allow publishing of content to multiple websites at once.
    
    This interface can publish content to multiple websites with a single
    function call. All websites must be authenticated for the function to work,
    however.
    
    This class is a singleton, therefore it can be "instantiated" repeatedly,
    and each reference will refer to the same instance.
    """
    __metaclass__ = Singleton
    
    def __init__(self):
        # Constructor
        self.__housekeep_datastore()
        self.bots = {
            Sites.FACEBOOK: FacebookBot(settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET),
            Sites.TWITTER: TwitterBot(settings.TWITTER_KEY, settings.TWITTER_SECRET),
            Sites.GPLUS: GPlusBot(settings.GPLUS_APP_ID, settings.GPLUS_SECRET),
            Sites.TUMBLR: TumblrBot(settings.TUMBLR_APP_ID, settings.TUMBLR_SECRET)
        }
        for site, social_bot in self.bots.items():
            social_token = self.__get_token(site)
            if social_token:
                social_bot.authenticate(social_token.main_token, social_token.sub_token)
    
    @staticmethod
    def __parse_localhost_url(url):
        # Remove all references to localhost URLs
        # Some online services cannot handle localhost links.
        localhost_url = "yoogle.com"
        localhost_regex = r"(?:^|(?<=\w://))localhost(?=(?:(?::\d+)?/.*)?$)"
        
        new_url = re.sub(localhost_regex, localhost_url, url, re.IGNORECASE)
        
        return new_url
    
    @staticmethod
    def __housekeep_datastore():
        # Delete expired tokens
        SocialToken.objects.filter(expiry_date__lte=datetime.today()).delete()
    
    @staticmethod
    def __get_token(site):
        # Retrieve token for site from datastore
        social_tokens = SocialToken.objects.filter(site=site
        ).exclude(expiry_date__lte=datetime.today()
        )
        
        if len(social_tokens) > 0:
            return social_tokens[0]
        else:
            return None
    
    @staticmethod
    def __clear_token(site):
        # Delete token for site from datastore
        SocialToken.objects.filter(site=site).delete()
    
    @staticmethod
    def __save_token(site, main_token, sub_token=None, expiry_date=None):
        # Save a new token for a site
        social_token = SocialToken(site=site, main_token=main_token, sub_token=sub_token, expiry_date = expiry_date)
        social_token.save()
    
    def get_sites(self):
        """Retrieves all sites managed by this SocialCenter instance.
        
        @rtype: dict
        @return: A dictionary, with site IDs as keys and nested dicts
                 as values. Each nested dict will contain metadata relevant
                 to the site, e.g.:
                 {
                    "aSite": {
                        "is_logged_in": false,
                        "name": "A Site"
                    },
                    "anotherSite": {
                        "is_logged_in": true,
                        "name": "Another site",
                        "account_name": "A Page",
                        "account_url": "http://anothersite.com/apage"
                    },
                 }
        """
        sites = {}
        for id, bot in self.bots.items():
            site_info = {}
            site_info["is_logged_in"] = self.is_logged_in(id)
            site_info["name"] = bot.get_site_name()
            if site_info["is_logged_in"]:
                site_info["account_name"] = bot.get_account_name()
                site_info["account_url"] = bot.get_account_url()
            sites[id] = site_info
        return sites
    
    def add_site(self, site, social_bot):
        """Adds a new C{SocialBot} to be managed by the SocialCenter.
        
        @type site: str
        @type social_bot: L{SocialBot}
        
        @param site: The ID of a site.
        @param social_bot: A L{SocialBot} that can interface with the site.
        
        @raise ValueError: Site ID is invalid, or a L{SocialBot} is not provided.
        """
        if not isinstance(social_bot, SocialBot):
            raise ValueError("A SocialBot must be provided!")
        if site and isinstance(site, str):
            self.bots[site] = social_bot
            # Authenticate the bot if an entry exists in the datastore
            social_token = self.__get_token(site)
            if social_token:
                social_bot.authenticate(social_token.main_token,
                                        social_token.sub_token)
        else:
            raise ValueError("A valid site name must be provided!")
    
    def remove_site(self, site):
        """Removes support for the given site.
        
        @type site: str
        
        @param site: The ID of a site.
        """
        if site in self.bots:
            del self.bots[site]
    
    def has_site(self, site):
        """Determines whether a site is supported.
        
        @type site: str
        
        @param site: The ID of a site.
        
        @rtype: bool
        @return: Whether the site is supported by the SocialCenter.
        """
        return site in self.bots
    
    def is_logged_in(self, site):
        """Determines whether a site is logged in.
        
        @type site: str
        
        @param site: The ID of a site.
        
        @rtype: bool
        @return: Whether the site is currently logged in.
        """
        num_of_tokens = SocialToken.objects.filter(site=site
        ).exclude(expiry_date__lte=datetime.today()
        ).count()
        return num_of_tokens > 0
    
    def must_select_page(self, site):
        """Determines whether a site requires page selection.
        
        @type site: str
        
        @param site: The ID of a site.
        
        @rtype: bool
        @return: Whether the site requires page selection.
        """
        return self.bots[site].must_select_page()
    
    def get_site_name(self, site):
        """Queries the full name of a site.
        
        @type site: str
        
        @param site: The ID of a site.
        
        @rtype: str
        @return: The full name of the site.
        """
        return self.bots[site].get_site_name()
    
    def get_client_token_name(self, site):
        """Queries the OAuth client token name of a site.
        
        @type site: str
        
        @param site: The ID of a site.
        
        @rtype: bool
        @return: The OAuth client token name.
        """
        return self.bots[site].get_client_token_name()
    
    def get_account_name(self, site):
        """Queries the account name logged into a site.
        
        @type site: str
        
        @param site: The ID of a site.
        
        @rtype: bool
        @return: The account name. If the site has not been logged
                 into yet, it will return "Unauthorized".
        """
        return self.bots[site].get_account_name()
    
    def get_account_url(self, site):
        """Queries the URL of an account logged into a site.
        
        @type site: str
        
        @param site: The ID of a site.
        
        @rtype: bool
        @return: The account URL. If the site has not been logged
                 into yet, it will return a blank string.
        """
        return self.bots[site].get_account_url()
        
    def process_client_token(self, site, token, auth_data):
        """Processes the client token for a site
        
        @type site: str
        @type token: str
        @type auth_data: dict
        
        @param site: The ID of a site.
        @param token: The client token retrieved from the site.
        @auth_data: The authentication data returned by C{start_authentication}
        
        @rtype: dict
        @return: A dictionary containing the tokens used by the site.
                 The tokens can either be used immediately via
                 C{authenticate}, or used to retrieve the account
                 pages first via C{get_pages}.
        """
        result = self.bots[site].process_token(token, auth_data)
        return result
    
    def authenticate(self, site, main_token, sub_token=None):
        """Authenticates the site with the given tokens.
        
        @type site: str
        @type main_token: str
        @type sub_token: str
        
        @param site: The ID of a site.
        @param token: The main token used for authentication.
        @auth_data: An optional secondary token used for authentication.
        
        @rtype: dict
        @return: A dictionary containing the tokens used by the site.
        """
        result = self.bots[site].authenticate(main_token, sub_token)
        if "main_token" in result:
            self.__save_token(site, result["main_token"],
                            result.get("sub_token", None),
                            result.get("expiry_date", None))
        return result
    
    def start_authentication(self, site, callback_url):
        """Begins the authentication process for a site.
        
        @type site: str
        @type callback_url: str
        
        @param site: The ID of a site.
        @param callback_url: The URL of the local page which can respond
                             to authentication responses.
        
        @rtype: dict
        @return: A dictionary containing authentication data which
                 must be used with C{process_client_token} later.
        """
        if site in self.bots:
            return self.bots[site].start_authentication(callback_url)
        else:
            return None, None
    
    def get_pages(self, site, request_token):
        """Retrieves all pages hosted by the authenticated site.
        
        @type site: str
        @type  request_token: str
        
        @param site: The ID of a site.
        @param request_token: The token used for requests to the website.
        
        @rtype: list
        @return: A list of dicts containing page information. For example:
            [
                {"id": "3415", "name": "A Page",
                 "id": "326662", "name": "Another Page"},
                ...
            ]
        """
        return self.bots[site].get_pages(request_token)
    
    def publish(self, title, content, link, site=None):
        """Publishes content to one or all sites managed by the SocialCenter.
        
        Publishes content to one or all sites, depending on whether site is
        set. If a website has not been logged in prior to this function call,
        the SocialCenter will not attempt to publish to it.
        
        @type title: str
        @type content: str
        @type link: str
        @type site: str
        
        @param title: The title of the post.
        @param content: A string containing the main body of the post.
        @param link: A link to a related resource
        @param site: An optional argument indicating the site to publish on.
            
        @rtype: dict
        @return: A dictionary containing all the returned data from the
            website(s). If an error is returned, the dict will contain the
            "error" key. For example:
            {
                "aSite": {
                    ...
                    "error" : "Unable to publish to website!",
                    ...
                }
            }
        """
        if link:
            link = self.__parse_localhost_url(link)
        if site:
            if self.is_logged_in(site):
                result = self.bots[site].post(title, content, link)
                result["name"] = self.get_site_name(site)
                return result
        else:
            results = {}
            async_results = {}
            pool = ThreadPool(processes=1)
            for social_site, social_bot in self.bots.items():
                results[social_site] = {
                    "logged_in" : self.is_logged_in(social_site),
                    "name"      : self.get_site_name(social_site)
                }
                if self.is_logged_in(social_site):
                    # Publish to different sites on separate threads
                    async_results[social_site] = pool.apply_async(social_bot.post,
                                                    (title, content, link))
                    # result = social_bot.post(title, content, link)
                    # merge results from individual bots with existing values
                    # results[social_site] = dict(result.items() + results[social_site].items())
            # Retrieve results from threads
            for social_site, async_result in async_results.items():
                # logger.debug("Retrieving results from %s" % social_site)
                result = async_result.get()
                results[social_site] = dict(result.items() + results[social_site].items())
                logger.debug("Published on %s!" % self.get_site_name(social_site))
            return results
        return None
        
    def logout(self, site):
        """Removes all authenitcation tokens associated with the site.
        
        @type site: str
        @param site: The ID of a site.
        """
        self.__clear_token(site)
        self.bots[site].clear_token()

class Sites:
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    GPLUS = "gplus"
    TUMBLR = "tumblr"