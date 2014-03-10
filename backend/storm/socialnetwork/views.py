from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST

from socialcenter import SocialCenter, Sites
import json
import logging
import facebook

logger = logging.getLogger('storm')

def social(request):
    social_center = SocialCenter()
    is_logged_into_twitter = social_center.is_logged_in(Sites.TWITTER)
    is_logged_into_facebook = social_center.is_logged_in(Sites.FACEBOOK)
    return render(request, "base.html", {
        "social_post_uri" : reverse('socialnetwork.views.social_post'),
        "facebook_redirect_uri" : reverse('socialnetwork.views.facebook_page_select'),
        "facebook_app_id" : settings.FACEBOOK_APP_ID,
        "is_logged_into_twitter" : is_logged_into_twitter,
        "is_logged_into_facebook" : is_logged_into_facebook
    })

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
            "rootURI" : reverse("socialnetwork.views.social"),
            "facebookProcessURI" : reverse("socialnetwork.views.facebook_process")
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
    if "access_token" in result:
        return HttpResponse("OK")
    else:
        return HttpResponseServerError("Server error")