from django.conf import settings
from models import SocialToken
from datetime import datetime
import logging

from socialbot import FacebookBot, TwitterBot, GPlusBot

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
    __metaclass__ = Singleton
    
    def __init__(self):
        logger.debug("Creating new instance of SocialCenter")
        self.housekeep_datastore()
        self.bots = {
            Sites.FACEBOOK: FacebookBot(settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET),
            Sites.TWITTER: TwitterBot(settings.TWITTER_KEY, settings.TWITTER_SECRET),
            Sites.GPLUS: GPlusBot(settings.GPLUS_APP_ID, settings.GPLUS_SECRET)
        }
        for site, social_bot in self.bots.items():
            social_token = self.get_token(site)
            if social_token:
                social_bot.authenticate(social_token.main_token, social_token.sub_token)
    
    @staticmethod
    def housekeep_datastore():
        # Delete expired tokens
        SocialToken.objects.filter(expiry_date__lte=datetime.today()).delete()
    
    @staticmethod
    def get_token(site):
        social_tokens = SocialToken.objects.filter(site=site
        ).exclude(expiry_date__lte=datetime.today()
        )
        
        if len(social_tokens) > 0:
            return social_tokens[0]
        else:
            return None
    
    @staticmethod
    def clear_token(site):
        SocialToken.objects.filter(site=site).delete()
    
    @staticmethod
    def save_token(site, main_token, sub_token=None, expiry_date=None):
        social_token = SocialToken(site=site, main_token=main_token, sub_token=sub_token, expiry_date = expiry_date)
        social_token.save()
    
    def is_logged_in(self, site):
        num_of_tokens = SocialToken.objects.filter(site=site
        ).exclude(expiry_date__lte=datetime.today()
        ).count()
        return num_of_tokens > 0
        
    def process_client_token(self, site, token, **kwargs):
        result = self.bots[site].process_token(token, **kwargs)
        return result
    
    def authenticate(self, site, main_token, sub_token=None):
        result = self.bots[site].authenticate(main_token, sub_token)
        if "main_token" in result:
            self.save_token(site, result["main_token"],
                            result.get("sub_token", None),
                            result.get("expiry_date", None))
        return result
    
    def start_authentication(self, site, callback_url):
        return self.bots[site].start_authentication(callback_url)
    
    def get_pages(self, site, request_token):
        return self.bots[site].get_pages(request_token)
    
    def publish(self, title, content, link, site=None):
        """Publishes content to one or all sites managed by the SocialCenter.
        
        Publishes content to one or all sites, depending on whether site is
        set.
        
        @type title: str
        @type content: str
        @type link: str
        @type site: str
        
        @param title: The title of the post.
        @param content: A string containing the main body of the post.
        @param link: A link to a related resource
        @param site: An optional argument indicating the site to publish on.
            
        @rtype: list
        @return: A list of dicts containing all the returned data from the
            website(s). If an error is returned, the dict will contain the
            "error" key. For example:
            [
                {
                    "site": "blogThis"
                    "result":
                        {
                         ...
                         "error" : "Unable to publish to website!",
                         ...
                        }
                }
            ]
        """
        if site:
            if self.is_logged_in(site):
                result = self.bots[site].post(title, content, link)
                return [{ "site" : site, "result" : result }]
        else:
            results = []
            for social_site, social_bot in self.bots.items():
                if self.is_logged_in(social_site):
                    result = social_bot.post(title, content, link)
                    results.append({ "site" : social_site, "result" : result })
            return results
        return None
        
    def logout(self, site):
        self.clear_token(site)
        self.bots[site].clear_token()

class Sites:
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    GPLUS = "gplus"