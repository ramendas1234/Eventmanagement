from django.contrib import admin
from .models import Event, City
from django.conf import settings

@admin.register(City)
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	search_fields = ['title','description']
	fieldsets = (
		('Event summary', {
			'fields': ( 'title', 'description','author','event_type')
			}),
		('Time', {
			'fields': ( 'event_start_date', 'event_end_date')
			}),
		('Event Venue', {
			'fields': ( 'event_venue', )
			}),
		('Event Location', {
			'fields': ( 'event_location', 'city','address','latitude','longitude'),'classes': ['location-meta']
			}),
		)

	class Media:
		css = {
		'all': ('css/admin/location_picker.css',)
		}
		js = ('https://maps.googleapis.com/maps/api/js?key={}&libraries=places'.format(settings.GOOGLE_MAPS_API_KEY),'js/admin/custom_backend.js', )