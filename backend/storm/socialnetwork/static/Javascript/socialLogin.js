jQuery.noConflict();

function loginToFacebook() {
    FB.login(function(response) {
      console.log(response);
      if (response.status === 'connected') {
        window.location.href = settings.facebookRedirectURI;
      }
    }, { scope: "manage_pages,status_update" });
}

jQuery(document).ready(function() {
  jQuery.ajaxSetup({ cache: true });
  
  jQuery.getScript('//connect.facebook.net/en_UK/all.js', function(){
    FB.init({
      appId      : settings.facebookAppId,
      cookie     : true
    });
    jQuery('#facebook-login').click(loginToFacebook);
    FB.Event.subscribe('auth.authResponseChange', function(response) {
      console.log(response);
    });
  });
  
});