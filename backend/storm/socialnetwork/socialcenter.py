from django.conf import settings
from models import SocialToken
from datetime import datetime
import logging

from socialbot import FacebookBot, TwitterBot

logger = logging.getLogger('storm')

class Singleton(type):
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
            Sites.TWITTER: FacebookBot(settings.TWITTER_KEY, settings.TWITTER_SECRET)
        }
        for site, social_bot in self.bots.items():
            social_token = self.get_token(site)
            if social_token:
                social_bot.set_token(social_token.main_token, social_token.sub_token)
    
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
    def save_token(site, main_token, sub_token, expiry_date):
        social_token = SocialToken(site=site, main_token=main_token, sub_token=sub_token, expiry_date = expiry_date)
        social_token.save()
    
    def is_logged_in(self, site):
        num_of_tokens = SocialToken.objects.filter(site=site
        ).exclude(expiry_date__lte=datetime.today()
        ).count()
        return num_of_tokens > 0
        
    def process_client_token(self, site, token, **kwargs):
        result = self.bots[site].process_token(token, **kwargs)
        if "main_token" in result:
            main_token = result["main_token"]
            sub_token = result.get("sub_token", None)
            expiry_date = result.get("expiry_date", None)
            self.clear_token(site)
            self.save_token(site, main_token, sub_token, expiry_date)
        return result
    
    def publish(self, title, content, link, site=None):
        if site:
            if self.is_logged_in(site):
                return self.bots[site].post(title, content, link)
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