var map;
var geocoder;
var iconBase = "http://localhost:8000/static/Map UI/";
var jsonBase = "http://localhost:8000/event/map/";
//var singaporeBound = "1.1679031235897843, 103.59146118164062|1.4569047431701578, 104.02507781982422";
var southWest = new google.maps.LatLng(1.1679031235897843, 103.59146118164062);
var northEast = new google.maps.LatLng(1.4569047431701578, 104.02507781982422);
var bound = new google.maps.LatLngBounds(southWest, northEast);
infowindow = new google.maps.InfoWindow();
var currentTime = new Date();
function initialize() {
    geocoder = new google.maps.Geocoder();
    map = new google.maps.Map(document.getElementById('map_canvas'), {
      zoom: 11,
      center: new google.maps.LatLng(1.3667,103.81),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var homeControlDiv = document.createElement('div');
    var homeControl = new HomeControl(homeControlDiv, map);

    homeControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(homeControlDiv);
    
    
    
    var icons = {
          Fire: {
            name: 'Fire',
            icon: iconBase + 'Fire.png'
          },
          Dengue: {
            name: 'Dengue',
            icon: iconBase + 'Dengue.png'
          },
          Gas_Leak: {
            name: 'Gas leaking',
            icon: iconBase + 'Gas_Leak.png'
          },
          Accident:{
            name:'Accident',
            icon: iconBase + 'Accident.png'
        }
        };

    loadEvent("data.json");
    function loadEvent(jsonName)
    {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', jsonBase, true);
        xhr.onload = function() {
          loadMarker(this.responseText);
        };
        xhr.send(); 
    }
    function loadMarker(results)
    {
        var json = JSON.parse(results);
        for(var key in json)
        {
            for (var i = 0; i < json[key].length; i++) {
                var data = json[key][i];
                var postalCode = data.postal_code;
                var reporter = data.reporter;
                var addr = data.address;
                var time = data.time;
                var des = data.description;
                if(postalCode!==''){
                    console.log(postalCode);
                    (function(postalCode, des, reporter, addr, time, key){
                        geocoder.geocode({ 'address': postalCode}, function(results, status) {
                            addMarker(des, reporter, addr, time, results[0].geometry.location, key);
                        });
                    })(postalCode,des,reporter, addr, time, key);
                }
                else{
                    (function(postalCode, des, reporter, addr, time, key){
                        geocoder.geocode({ 'address': addr, 'bounds':bound}, function(results, status) {
                            addMarker(des, reporter, addr, time, results[0].geometry.location, key);

                        });
                    })(postalCode,des,reporter, addr, time, key);
                }

            }
        }
   }

    function addMarker(description, reporter, addr, time, location, key)
    {

        var eventTime = new Date(time);
        var diff = Math.round((currentTime - eventTime)/3600000);
        var marker = new google.maps.Marker({
            map: map,
            position: location,
            icon: iconBase + key + ".png",
            animation: google.maps.Animation.DROP
        });
        if(diff<3)
            marker.setAnimation(google.maps.Animation.BOUNCE)
//        google.maps.event.addListener(marker, 'click', toggleBounce);
		var newDes = description.substring(0,60);
        var content = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<h4 id="firstHeading" class="firstHeading">'+icons[key].name+'</h4>'+
      '<div id="bodyContent">'+
      '<b>Name of reporter: </b>' + reporter + 
      '<br><b>Venue: </b>' + addr +
      '<br><b>Time reported: </b>'+ time+
      '<br><b>Description: </b>' + newDes + ' ...'
      '</div>'+
      '</div>';
        google.maps.event.addListener(marker, 'click', function () {
			infowindow.setOptions({maxWidth:200});
            infowindow.setContent(content);
            infowindow.open(map, marker);
        });
    }
//    function toggleBounce()
//    {
//        if(marker.getAnimation()!= null)
//            marker.setAnimation(null);
//        else
//            marker.setAnimation(google.maps.Animation.Bounce);
//    }
    //create legend
//   var legend = document.createElement('div');
//    legend.id = 'legend';
//    var content = [];
//    content.push('<h3>Legend</h3>');
//    for(var key in icons)
//    {
//        var type = icons[key];
//        var name = type.name;
//        var icon = type.icon;
//        content.push('<p> <div> <img src="' + icon + '">'+ name+'</div></p>');
//    }
//    legend.innerHTML = content.join('');
//    legend.index = 1;
//    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
    //testing: get lat long
//    google.maps.event.addListener(map, "click", function(event)
//    {
//         alert("Latitude: " + event.latLng.lat()+ ", Longitude: "+event.latLng.lng());
//    });
//    }
}
google.maps.event.addDomListener(window, 'load', initialize);