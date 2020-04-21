from django.shortcuts import render
from .models import Event, City, Category
import datetime
from django.db.models import Q
# Create your views here.

def index(request):
	data = [];
	return render(request, 'index.html')
def location_based_events(request,city):
	now = datetime.datetime.now()
	city_data = City.objects.filter(name=city)
	if not city_data:
		return render(request, 'index.html')
	cityId = city_data[0].id
	events = Event.objects.filter(Q(city_id = cityId)& Q(event_end_date__gt=now) & Q(listing_type='public') )
	categories = Category.objects.values_list('id','name')
	data = {
	'events':events,
	'categories': categories
	}
	return render(request, 'city_events.html',{'data':data})
