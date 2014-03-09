jQuery.noConflict();

function loginToFacebook() {
    FB.login(function(response) {
      console.log(response);
      if (response.status === 'connected') {
        window.location.href = 'facebook';
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
  
  var postForm = jQuery("#postForm");
  postForm.submit(function(event) {
    event.preventDefault();
    var postTitle = postForm.find("input[name=postTitle]").val();
    var postContent = postForm.find("textarea[name=postContent]").val();
    var postLink = postForm.find("input[name=postLink]").val();
    jQuery.post("/social/post", {
        postTitle: postTitle,
        postContent: postContent,
        postLink: postLink
        })
        .done(function() {
            jQuery("#postStatus").text("Post successful!");
        })
        .fail(function() {
            jQuery("#postStatus").text("Post failed!");
        });
  });
});