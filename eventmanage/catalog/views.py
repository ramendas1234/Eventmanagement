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
def all_events(request):
	now = datetime.datetime.now()
	events = Event.objects.filter(Q(event_end_date__gt=now) & Q(listing_type='public') )
	categories = Category.objects.values_list('id','name')
	online_events = Event.objects.filter( Q(event_end_date__gt=now) & Q(listing_type='public') & Q(event_venue='online') )
	data = {
	'events':events,
	'categories': categories,
	'online_events':online_events
	}
	return render(request, 'all_events.html',{'data':data})

def all_events_filter(request):
	now = datetime.datetime.now()
	time = request.POST.get('filterby_time','')
	catgid = request.POST.get('filterby_category','')
	listing_type = request.POST.get('listing_type','')
	sortby = request.POST.get('sort_by','')
	events = Event.objects.filter( Q(event_end_date__gt=now) & Q(listing_type='public') )
	if(time):
		time = int(time)
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta( days = time )
		events = events.filter(event_start_date__lte = tomorrow)
		# events = events.filter(event_start_date__week_day__gte=5)
	if(catgid):
		events = events.filter(Q(category = catgid))
	if(listing_type):
		events = events.filter(Q(event_venue = listing_type))	
	html = render_to_string('hello_world.html', {'events': events})

	return HttpResponse(html)

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
	'categories': categories,
	'city': city_data[0]
	}
	return render(request, 'city_events.html',{'data':data})

def event_filtration(request,city):
	now = datetime.datetime.now()
	city_data = City.objects.filter(name=city)
	if not city_data:
		return render(request, 'index.html')
	cityId = city_data[0].id
	time = request.POST.get('filterby_time','')
	catgid = request.POST.get('filterby_category','')
	listing_type = request.POST.get('listing_type','')
	sortby = request.POST.get('sort_by','')
	events = Event.objects.filter( Q(city_id = cityId)& Q(event_end_date__gt=now) & Q(listing_type='public') )
	if(time):
		time = int(time)
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta( days = time )
		events = events.filter(event_start_date__lte = tomorrow)
		# events = events.filter(event_start_date__week_day__gte=5)
	if(catgid):
		events = events.filter(Q(category = catgid))
	if(listing_type):
		events = events.filter(Q(event_venue = listing_type))	
	html = render_to_string('hello_world.html', {'events': events})

	return HttpResponse(html)
