var map;
var geocoder;
var iconBase = "http://localhost:8080/CMS/";
//"file:///C:/Users/Desmond%20Teo/Dropbox/CZ%203003%20Front%20End%20Team/Front%20End%20Page/businessnewswebtemplate/Map UI/";
var jsonBase = "http://localhost:8080/CMS/";
//"file:///C:/Users/Desmond%20Teo/Dropbox/CZ%203003%20Front%20End%20Team/Front%20End%20Page/businessnewswebtemplate/Map UI/";

infowindow = new google.maps.InfoWindow();
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
            icon: iconBase + 'fire.png'
          },
          Dengue: {
            name: 'Dengue',
            icon: iconBase + 'dengue.png'
          },
          Gas_leak: {
            name: 'Gas leaking',
            icon: iconBase + 'gas_leak.png'
          },
    /*      Earthquake:{
            name:'Earthquake',
            icon: iconBase + 'earthquake.png'
          },
          Tsunami:{
            name:'Tsunami',
            icon: iconBase + 'tsunami.png'
          },
          Treedown:{
            name:'Tree down',
            icon: iconBase + 'treedown.png'
          },
          Tornado:{
            name:'Tornado',
            icon: iconBase + 'tornado.png'
          }
		  */
        };

    loadEvent("fire.png", "fire.json");
    loadEvent("dengue.png", "dengue.json");
    loadEvent("gas_leak.png","gas_leak.json");

    function loadEvent(iconName, jsonName)
    {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', jsonBase+jsonName, true);
        xhr.onload = function() {
          loadMarker(this.responseText, iconName);
        };
        xhr.send(); 
    }
    function loadMarker(results, iconName)
    {
        var json = JSON.parse(results);
        var location;
        for (var i = 0; i < json.length; i++) {
            var postalCode = json[i].postal_code;
            var data = json[i];
            var stt = data.status;
            (function(postalCode, stt){
                geocoder.geocode({ 'address': postalCode}, function(results, status) {
                    addMarker(stt, results[0].geometry.location, iconName);
                });
            })(postalCode,stt);

        }
   }

    function addMarker(status, location, iconName)
    {
        var marker = new google.maps.Marker({
            map: map,
            position: location,
            icon: iconBase + iconName 
        });
        google.maps.event.addListener(marker, 'click', function () {
            infowindow.setContent(status);
            infowindow.open(map, marker);
        });
    }
   var legend = document.createElement('div');
    legend.id = 'legend';
    var content = [];
    content.push('<h4>Legend</h4>');
    for(var key in icons)
    {
        var type = icons[key];
        var name = type.name;
        var icon = type.icon;
        content.push('<br> <div> <img src="' + icon + '">'+ name+'</div>');
    }
    legend.innerHTML = content.join('');
    legend.index = 1;
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
    //testing
    google.maps.event.addListener(map, "click", function(event)
    {
         alert("Latitude: " + event.latLng.lat()+ ", Longitude: "+event.latLng.lng());
    });
    }
google.maps.event.addDomListener(window, 'load', initialize);