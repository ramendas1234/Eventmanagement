from django.contrib import admin
from .models import Event, City, Category, Image, Tickit
from django.conf import settings

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
	pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	fieldsets = (
		('', {
			'fields': ( 'name', 'description','image_tag','image')
			}),
		
		)
	readonly_fields = ['image_tag']

class ImageInline(admin.StackedInline):
	model = Image
	extra = 0
	verbose_name_plural = "Image Galleries"
class TickitInline(admin.TabularInline):
	model = Tickit


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	# form = EventForm
	search_fields = ['title','description']
	inlines = [TickitInline,ImageInline]
	fieldsets = (
		('Event summary', {
			'fields': ( 'title', 'description','author','event_type','category')
			}),
		('Time', {
			'fields': ( 'event_start_date', 'event_end_date')
			}),
		('Event Image', {
			'fields': ( 'banner_image_tag', 'banner_image','thumb_image_tag','thumb_image'),
			}),
		('Event Venue', {
			'fields': ( 'event_venue', )
			}),
		('Event Location', {
			'fields': ( 'event_location', 'city','address','latitude','longitude'),'classes': ['location-meta']
			}),
		('Event Other information', {
			'fields': ( 'video_url', 'website_link','listing_type','featured',),
			}),

		)
	readonly_fields = ('banner_image_tag','thumb_image_tag',)
	def save_model(self, request, obj, form, change):
		# super(EventAdmin,self).save_model(request, obj, form, change)
		obj.save()

		for afile in request.FILES.getlist('photos_multiple'):
			obj.images.create(file=afile)

	class Media:
		css = {
		'all': ('css/admin/location_picker.css',)
		}
		js = ('https://maps.googleapis.com/maps/api/js?key={}&libraries=places'.format(settings.GOOGLE_MAPS_API_KEY),'js/admin/custom_backend.js', )

		