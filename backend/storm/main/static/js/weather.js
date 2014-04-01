var $items;
$.ajax({
	url : 	"http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20xml%20where%20url%3D%22http%3A//weather.yahooapis.com/forecastrss%3Fw%3D1062617%26u%3Dc%22&format=json", 
	async:false,
	dataType: "json",
	success: function (data) {
	console.log(data);
	items=data.query.results.rss.channel.item.description;  
	
  }
}); //end of ajax


$(function(){

 $("#weather").append(items);
 });