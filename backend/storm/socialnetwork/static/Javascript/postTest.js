jQuery.noConflict();

jQuery(document).ready(function() {
  // Prepare post publish test form for use.
  var postForm = jQuery("#postForm");
  var errorAlert = jQuery("#errorAlert");
  var successAlert = jQuery("#successAlert");
  // Submits the post details over a separate thread.
  postForm.submit(function(event) {
    event.preventDefault();
    
    var postTitle = postForm.find("input[name=postTitle]").val();
    var postContent = postForm.find("textarea[name=postContent]").val();
    var postLink = postForm.find("input[name=postLink]").val();
    
    var submitButton = postForm.find("input[type=submit]");
    
    jQuery(".alert").hide();
    submitButton.button("loading");
    
    jQuery.post(settings.socialPostURI, {
          postTitle: postTitle,
          postContent: postContent,
          postLink: postLink
        })
        .done(function() {
            successAlert.find("span").text("Post published in all sites!");
            successAlert.show();
        })
        .fail(function(response) {
            console.log(response)
            try {
                failedSites = JSON.parse(response.responseText);
                failedSiteNames = [];
                for (id in failedSites) {
                    if (failedSites.hasOwnProperty(id)) {
                        failedSiteNames.push(failedSites[id].name);
                    }
                }
                errorAlert.find("span").text("Post failed to publish in the following sites: " + failedSiteNames.join(", "));
            } catch(err) {
                errorAlert.find("span").text("Unknown error occurred!");
            }
            errorAlert.show();
        })
        .always(function() {
            submitButton.button("reset");
        });
  });
  
  jQuery('.alert .close').click(function() {
    jQuery(this).parent().hide();
    console.log("Done");
  });
});