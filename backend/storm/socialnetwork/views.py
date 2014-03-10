from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET, require_POST
import json
import logging

from socialcenter import SocialCenter, Sites
import facebook
from twython import Twython
from requests_oauthlib import OAuth2Session

logger = logging.getLogger('storm')

@require_GET
def social(request):
    social_center = SocialCenter()
    is_logged_into_facebook = social_center.is_logged_in(Sites.FACEBOOK)
    is_logged_into_twitter = social_center.is_logged_in(Sites.TWITTER)
    is_logged_into_gplus = social_center.is_logged_in(Sites.GPLUS)
    return render(request, "base.html", {
        "social_post_uri" : reverse('socialnetwork.views.social_post'),
        "facebook_redirect_uri" : reverse('socialnetwork.views.facebook_page_select'),
        "facebook_app_id" : settings.FACEBOOK_APP_ID,
        "twitter_auth_uri" : reverse('socialnetwork.views.twitter_auth'),
        "gplus_auth_uri" : reverse('socialnetwork.views.gplus_auth'),
        "is_logged_into_twitter" : is_logged_into_twitter,
        "is_logged_into_facebook" : is_logged_into_facebook,
        "is_logged_into_gplus" : is_logged_into_gplus,
        "facebook_logout_uri" : reverse('socialnetwork.views.social_logout', kwargs={ "site" : Sites.FACEBOOK }),
        "twitter_logout_uri" : reverse('socialnetwork.views.social_logout', kwargs={ "site" : Sites.TWITTER }),
        "gplus_logout_uri" : reverse('socialnetwork.views.social_logout', kwargs={ "site" : Sites.GPLUS }),
    })

@require_GET
def social_logout(request, site):
    social_center = SocialCenter()
    social_center.logout(site)
    return redirect('socialnetwork.views.social')

@require_POST
def social_post(request, site=None):
    logger.debug(request.POST)
    title = request.POST["postTitle"]
    content = request.POST["postContent"]
    link = request.POST["postLink"]
    social_center = SocialCenter()
    results = social_center.publish(title, content, link, site=site)
    logger.debug(results)
    if isinstance(results, list):
        failed_list = []
        for post_attempt in results:
            result = post_attempt["result"]
            if "error" in result:
                failed_list.append(post_attempt["site"])
        if failed_list:
            return HttpResponseServerError(json.dumps({ "error" : failed_list }))
    return HttpResponse("OK")

@require_GET
def facebook_page_select(request):
    #import pdb; pdb.set_trace()
    key = settings.FACEBOOK_APP_ID
    secret = settings.FACEBOOK_SECRET
    user = facebook.get_user_from_cookie(request.COOKIES, key, secret)
    displayed_pages = None
    if user:
        token = user["access_token"]
        request.session["fb_access_token"] = token
        
        graph = facebook.GraphAPI(token)
        pages = graph.get_object("me/accounts").get("data", None)
        
        if pages:
            displayed_pages = []
            for page in pages:
                displayed_page = {
                    "id" : page[u"id"],
                    "name" : page[u"name"]
                }
                displayed_pages.append(displayed_page)
        
        return render(request, "facebook.html", {
            "pages" : displayed_pages,
            "root_uri" : reverse("socialnetwork.views.social"),
            "facebook_process_uri" : reverse("socialnetwork.views.facebook_process")
        })
    else:
        logger.debug("No token")
    return redirect('socialnetwork.views.social')

@require_POST
def facebook_process(request):
    token = request.session["fb_access_token"]
    del request.session["fb_access_token"]
    page_id = request.POST["pageId"]
    social_center = SocialCenter()
    result = social_center.process_client_token(Sites.FACEBOOK, token, page_id=page_id)
    logger.debug(result)
    if "main_token" in result:
        return HttpResponse("OK")
    else:
        return HttpResponseServerError("Server error")

@require_GET
def twitter_auth(request):
    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    
    callback_url = request.build_absolute_uri(reverse("socialnetwork.views.twitter_callback"))
    auth = twitter.get_authentication_tokens(callback_url=callback_url)
    
    request.session["twitter_oauth_token"] = auth["oauth_token"]
    request.session["twitter_oauth_token_secret"] = auth["oauth_token_secret"]
    
    twitter_oauth_url = auth["auth_url"]
    return redirect(twitter_oauth_url)

@require_GET
def twitter_callback(request):
    if "denied" in request.GET:
        return HttpResponseServerError("ERROR: Access to Twitter was denied.")

    twitter_oauth_verifier = request.GET["oauth_verifier"]
    
    twitter_oauth_token = request.session["twitter_oauth_token"]
    twitter_oauth_secret = request.session["twitter_oauth_token_secret"]
    del request.session["twitter_oauth_token"]
    del request.session["twitter_oauth_token_secret"]
    
    social_center = SocialCenter()
    result = social_center.process_client_token(Sites.TWITTER, twitter_oauth_verifier,
                                       oauth_token=twitter_oauth_token,
                                       oauth_secret=twitter_oauth_secret)
    logger.debug(result)
    if "main_token" in result:
        return redirect("socialnetwork.views.social")
    else:
        return HttpResponseServerError(result["error"])

@require_GET
def gplus_auth(request):
    
    callback_url = request.build_absolute_uri(reverse("socialnetwork.views.gplus_callback"))
    oauth_session = OAuth2Session(settings.GPLUS_APP_ID, redirect_uri=callback_url)
    
    gplus_auth_url, state = oauth_session.authorization_url('https://bufferapp.com/oauth2/authorize')
    
    return redirect(gplus_auth_url)

@require_GET
def gplus_callback(request):
    if "error" in request.GET:
        return HttpResponseServerError("ERROR: " + request.GET["error"])
    
    gplus_auth_code = request.GET["code"]

    gplus_callback_url = request.build_absolute_uri(reverse("socialnetwork.views.gplus_callback"))
    
    social_center = SocialCenter()
    import pdb; pdb.set_trace()
    result = social_center.process_client_token(Sites.GPLUS, gplus_auth_code,
                                       callback_url=gplus_callback_url)
    logger.debug(result)
    if "main_token" in result:
        return redirect("socialnetwork.views.social")
    else:
        return HttpResponseServerError(result["error"])