django.jQuery(document).ready(function($){

 var prev_el_selector = '.form-row.field-address';
  // If we don't have a lat/lon in the input fields,
  // this is where the map will be centered initially.
  event_lat_val = $('#id_latitude').val();
  event_lng_val = $('#id_longitude').val();
  var initial_lat = (!event_lat_val)?51.516448:parseInt(event_lat_val),
      initial_lon = (!event_lng_val)?-0.130463:parseInt(event_lng_val);
  // The input elements we'll put lat/lon into and use
  // to set the map's initial lat/lon.
  var lat_input_selector = '#id_latitude',
      lon_input_selector = '#id_longitude';    

  // Initial zoom level for the map.
  var initial_zoom = 8;

  // Initial zoom level if input fields have a location.
  var initial_with_loc_zoom = 12;

  // Global variables. Nice.
  var map, marker, $lat, $lon;

function initMap(){
	var $prevEl = $(prev_el_selector);
	$lat = $(lat_input_selector);
    $lon = $(lon_input_selector);

    if ($prevEl.length === 0) {
      // Can't find where to put the map.
      return;
    };
    $prevEl.after( $('<div class="js-setloc-map setloc-map"></div>') );
    var mapEl = document.getElementsByClassName('js-setloc-map')[0];
    var latlng = new google.maps.LatLng($lat.val(),$lon.val());

    map = new google.maps.Map(mapEl, {
      zoom: initial_zoom,
      center: {lat: initial_lat, lng: initial_lon}
    });

    var input = document.getElementById('id_address');
    var autocomplete = new google.maps.places.Autocomplete(input);
    var marker = new google.maps.Marker({
          position: new google.maps.LatLng($lat.val(), $lon.val()),
          map: map,
          anchorPoint: new google.maps.Point(0, -29)
        });

    autocomplete.addListener('place_changed',function(){
    	marker.setVisible(false);
    	var place = autocomplete.getPlace();
    	if (!place.geometry) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            window.alert("No details available for input: '" + place.name + "'");
            return;
          }
          // If the place has a geometry, then present it on a map.
          if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
          } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);  // Why 17? Because it looks good.
          }
          marker.setPosition(place.geometry.location);
          marker.setVisible(true);
          // console.log(marker.getPosition().lat())
          // console.log(marker.getPosition().lng())
          setInputValues(marker.getPosition().lat(), marker.getPosition().lng());


    });

      /**
   * Set both lat and lon input values.
   */
  function setInputValues(lat, lon) {
    setInputValue($lat, lat);
    setInputValue($lon, lon);
  };
  /**
   * Set the value of $input to val, with the correct decimal places.
   * We work out decimal places using the <input>'s step value, if any.
   */
  function setInputValue($input, val) {
    // step should be like "0.000001".
    var step = $input.prop('step');
    var dec_places = 0;

    if (step) {
      if (step.split('.').length == 2) {
        dec_places = step.split('.')[1].length;
      };

      val = val.toFixed(dec_places);
    };

    $input.val(val);
  };
}


/*var input = document.getElementById('id_address');
      var autocomplete = new google.maps.places.Autocomplete(input,{types: ['(cities)']});
      google.maps.event.addListener(autocomplete, 'place_changed', function(){
         var place = autocomplete.getPlace();
         console.log(place)
      }); */
initMap();

if($('#id_event_venue').val() == 'venue'){
  $('.location-meta').show();
}else{
  $('.location-meta').hide();
}

$(document).on('change','#id_event_venue',function(){
	var venue_type = $(this).val() ;
	if(venue_type == 'venue'){
		$('.location-meta').show();
	}else{
		$('.location-meta').hide();
	}
});

});