from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET, require_POST
import json
import logging

from socialcenter import SocialCenter, Sites
from requests_oauthlib import OAuth2Session

logger = logging.getLogger('storm')

@require_GET
def social(request):
    social_center = SocialCenter()
    is_logged_into_facebook = social_center.is_logged_in(Sites.FACEBOOK)
    is_logged_into_twitter = social_center.is_logged_in(Sites.TWITTER)
    is_logged_into_gplus = social_center.is_logged_in(Sites.GPLUS)
    return render(request, "base.html", {
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
def social_post_test(request):
    return render(request, "postTest.html", {
        "social_post_uri" : reverse('socialnetwork.views.social_post')
    })

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
def social_logout(request, site):
    social_center = SocialCenter()
    social_center.logout(site)
    return redirect('socialnetwork.views.social')

@require_GET
def facebook_page_select(request):
    #import pdb; pdb.set_trace()
    app_id = settings.FACEBOOK_APP_ID
    cookie_id = "fbsr_" + app_id
    if cookie_id not in request.COOKIES:
        return HttpResponseServerError("Facebook cookie not found")
    fb_cookie = request.COOKIES[cookie_id]
    
    social_center = SocialCenter()
    result = social_center.process_client_token(Sites.FACEBOOK, { cookie_id : fb_cookie })
    
    if "main_token" not in result:
        return HttpResponseServerError("Could not retrieve token")
    
    main_token = result["main_token"]
    request.session["fb_access_token"] = main_token
    
    pages = social_center.get_pages(Sites.FACEBOOK, main_token)
        
    return render(request, "selectPage.html", {
        "pages" : pages,
        "root_uri" : reverse("socialnetwork.views.social"),
        "process_uri" : reverse("socialnetwork.views.facebook_process")
    })

@require_POST
def facebook_process(request):
    main_token = request.session["fb_access_token"]
    del request.session["fb_access_token"]
    
    page_id = request.POST["pageId"]
    
    social_center = SocialCenter()
    result = social_center.authenticate(Sites.FACEBOOK, main_token, page_id)
    
    logger.debug(result)
    
    if "main_token" in result:
        return HttpResponse("OK")
    else:
        return HttpResponseServerError("Server error")

@require_GET
def twitter_auth(request):
    
    callback_url = request.build_absolute_uri(reverse("socialnetwork.views.twitter_callback"))
    
    social_center = SocialCenter()
    oauth_url, auth_data = social_center.start_authentication(Sites.TWITTER, callback_url)
    
    request.session["twitter_oauth_token"] = auth_data["twitter_oauth_token"]
    request.session["twitter_oauth_token_secret"] = auth_data["twitter_oauth_token_secret"]
    
    return redirect(oauth_url)

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
        social_center.authenticate(Sites.TWITTER,
                                    result["main_token"],
                                    result.get("sub_token", None))
        return redirect("socialnetwork.views.social")
    else:
        return HttpResponseServerError(result["error"])

@require_GET
def gplus_auth(request):
    
    callback_url = request.build_absolute_uri(reverse("socialnetwork.views.gplus_callback"))
    
    social_center = SocialCenter()
    oauth_url, auth_data = social_center.start_authentication(Sites.GPLUS, callback_url)
    
    return redirect(oauth_url)

@require_GET
def gplus_callback(request):
    if "error" in request.GET:
        return HttpResponseServerError("ERROR: " + request.GET["error"])
    
    gplus_auth_code = request.GET["code"]
    
    callback_url = request.build_absolute_uri(reverse("socialnetwork.views.gplus_callback"))
    
    social_center = SocialCenter()
    result = social_center.process_client_token(Sites.GPLUS, gplus_auth_code,
                                        callback_url=callback_url)
    logger.debug(result)
    
    if "main_token" not in result:
        return HttpResponseServerError("Could not retrieve token")
    
    main_token = result["main_token"]
    request.session["gplus_access_token"] = main_token
    
    pages = social_center.get_pages(Sites.GPLUS, main_token)
        
    return render(request, "selectPage.html", {
        "pages" : pages,
        "root_uri" : reverse("socialnetwork.views.social"),
        "process_uri" : reverse("socialnetwork.views.gplus_process")
    })

@require_POST
def gplus_process(request):
    main_token = request.session["gplus_access_token"]
    del request.session["gplus_access_token"]
    
    page_id = request.POST["pageId"]
    
    social_center = SocialCenter()
    result = social_center.authenticate(Sites.GPLUS, main_token, page_id)
    
    logger.debug(result)
    
    if "main_token" in result:
        return HttpResponse("OK")
    else:
        return HttpResponseServerError("Server error")