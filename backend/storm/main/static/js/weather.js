// Author: Muhammad Fazli Bin Rosli
// Matriculation No.: N1302335L
// Functionality: Weather Forecast
jQuery(function() {
    var weatherImageURL = "http://l.yimg.com/a/i/us/we/52/";
    var weatherImageExt = ".gif";
    jQuery.ajax({
        url : 	"http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20xml%20where%20url%3D%22http%3A//weather.yahooapis.com/forecastrss%3Fw%3D1062617%26u%3Dc%22&format=json", 
        dataType: "json",
        success: function (data) {
            var list = jQuery("<ul class=\"weather\"/>");
            console.log(data);
            var forecasts = data.query.results.rss.channel.item.forecast;
            for (var i = 0; i < forecasts.length; i++) {
                if (i == 0) forecasts[i].day = "Today";
                var weatherImage = weatherImageURL + forecasts[i].code + weatherImageExt;
                var listItem = jQuery("<li/>");
                var imageElement = jQuery('<img src="' + weatherImage + '" width="25px" height="25px" title="' + forecasts[i].text + '" />');
                jQuery("<span/>", {
                    text: forecasts[i].day
                }).appendTo(listItem);
                jQuery("<span/>", {
                    text: forecasts[i].low + "/" + forecasts[i].high,
                    "class": "forecast"
                }).append(imageElement).appendTo(listItem);
                list.append(listItem);
            }
            $("#weather").append(list);
        },
        error: function() {
            console.log("Failed to load Weather");
            $("#weather").text("Unable to load weather data");
        }
    });

});