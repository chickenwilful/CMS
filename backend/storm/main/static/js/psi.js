// Author: Muhammad Fazli Bin Rosli
// Matriculation No.: N1302335L
// Functionality: PSI Levels
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