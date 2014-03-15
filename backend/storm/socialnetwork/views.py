from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET, require_POST
import json
import logging

from socialcenter import SocialCenter, Sites

logger = logging.getLogger('storm')

@require_GET
def social(request):
    social_center = SocialCenter()
    
    sites = social_center.get_sites()
    
    for site_id, site in sites.items():
        site["auth_uri"] = reverse("socialnetwork.views.social_auth", kwargs={ "site": site_id })
        site["logout_uri"] = reverse("socialnetwork.views.social_logout", kwargs={ "site": site_id })
    
    return render(request, "base.html", {
        "sites" : sites
    })

@require_GET
def social_test(request):
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
    if not social_center.has_site(site):
        return HttpResponseNotFound("Site not found")
    
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

@require_GET
def social_auth(request, site):
    
    callback_url = request.build_absolute_uri(reverse('socialnetwork.views.social_callback', kwargs={ "site" : site }))
    auth_data_key = "%s_auth_data" % site
    
    social_center = SocialCenter()
    if not social_center.has_site(site):
        return HttpResponseNotFound("Site not found")
    
    oauth_url, auth_data = social_center.start_authentication(site, callback_url)
    
    request.session[auth_data_key] = auth_data
    
    return redirect(oauth_url)

@require_GET
def social_callback(request, site):
    social_center = SocialCenter()
    
    if not social_center.has_site(site):
        return HttpResponseNotFound("Site not found")
    
    if "error" in request.GET:
        return HttpResponseServerError("ERROR: " + request.GET["error"])
    
    auth_data_key = "%s_auth_data" % site
    main_token_key = "%s_main_token" % site
    client_token_name = social_center.get_client_token_name(site)
    
    auth_data = request.session[auth_data_key]
    client_token = request.GET[client_token_name]
    
    del request.session[auth_data_key]
    
    result = social_center.process_client_token(site, client_token, auth_data)
    logger.debug(result)
    
    if "main_token" not in result:
        return HttpResponseServerError("Could not retrieve token")
    
    main_token = result["main_token"]
    
    if social_center.must_select_page(site):
        pages = social_center.get_pages(site, main_token)
        request.session[main_token_key] = main_token
            
        return render(request, "selectPage.html", {
            "pages" : pages,
            "root_uri" : reverse("socialnetwork.views.social"),
            "process_uri" : reverse("socialnetwork.views.social_page_select", kwargs={ "site" : site })
        })
    else:
        social_center.authenticate(site,
                                    main_token,
                                    result.get("sub_token", None))
        return redirect("socialnetwork.views.social")

@require_POST
def social_page_select(request, site):
    social_center = SocialCenter()
    
    if not social_center.has_site(site):
        return HttpResponseNotFound("Site not found")
    
    main_token_key = "%s_main_token" % site
    
    main_token = request.session[main_token_key]
    del request.session[main_token_key]
    
    page_id = request.POST["pageId"]
    
    social_center = SocialCenter()
    result = social_center.authenticate(site, main_token, page_id)
    
    logger.debug(result)
    
    if "main_token" in result:
        return HttpResponse("OK")
    else:
        return HttpResponseServerError("Server error")