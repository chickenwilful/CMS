$(function() {
  $.ajax({
    url : "/main/getPSI",
    dataType: "text",
    success: function(data) {
      console.log(data);
      $("#psi").append(data);
    },
    error: function() {
      console.log("Failed to load PSI");
      $("#psi").text("Unable to load PSI data");
    }
  });
});