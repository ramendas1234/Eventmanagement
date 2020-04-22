from django.http import HttpResponse
from django.core import serializers
import json
from django.template.loader import render_to_string
from urllib.parse import parse_qs  
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

def event_filtration(request,city):
	now = datetime.datetime.now()
	time = request.POST.get('filterby_time','')
	catgid = request.POST.get('filterby_category','')
	sortby = request.POST.get('sort_by','')
	events = Event.objects.filter( Q(event_end_date__gt=now) & Q(listing_type='public') )
	if(catgid):
		events = events.filter(Q(category = catgid))
	html = render_to_string('hello_world.html', {'events': events})

	return HttpResponse(html)
