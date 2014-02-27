$(document).ready(function() {
	console.log('Event.js');
	$.ajax('http://localhost:8000/event/', {
		'success': function(data) {
			console.log(data);
			events = data['data']['events'];
			$.each(events, function(index, value) {
				event_template = $('#event_template').html();
				for(key in value) {
					event_template = event_template.replace('$' + key + '$', value[key]);
				}
				$('#container').append($('div').html(event_template));
			});
		}
	});
});
