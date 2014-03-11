jQuery.noConflict();

jQuery(document).ready(function() {
  
  var postForm = jQuery("#postForm");
  postForm.submit(function(event) {
    event.preventDefault();
    var postTitle = postForm.find("input[name=postTitle]").val();
    var postContent = postForm.find("textarea[name=postContent]").val();
    var postLink = postForm.find("input[name=postLink]").val();
    jQuery.post(settings.socialPostURI, {
        postTitle: postTitle,
        postContent: postContent,
        postLink: postLink
        })
        .done(function() {
            jQuery("#postStatus").text("Post published in all sites!");
        })
        .fail(function(response) {
            responseData = JSON.parse(response.responseText);
            failedSites = responseData.error;
            jQuery("#postStatus").text("Post failed to publish in the following sites: " + failedSites.join());
        });
  });
});