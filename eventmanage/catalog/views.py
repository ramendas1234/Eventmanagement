from django.http import HttpResponse
from django.core import serializers
import json
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_text
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from urllib.parse import parse_qs  
from django.shortcuts import render, redirect
from .models import Event, City, Category
from .forms import SignUpForm
import datetime
from django.db.models import Q
from django.contrib import auth

from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

def signup_view(request):
	if request.user.is_authenticated:
		return redirect('index')
	if(request.method=='POST'):
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.first_name = form.cleaned_data.get('first_name')
			user.profile.last_name = form.cleaned_data.get('last_name')
			user.profile.email = form.cleaned_data.get('email')
			user.is_active = True
			user.save()
			current_site = get_current_site(request)
			subject = 'Please Activate Your Account'
			message = render_to_string('activation_request.html', {
			'user': user,
			'domain': current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			# method will generate a hash value with user related data
			'token': account_activation_token.make_token(user),
			})
			user.email_user(subject, message)
			# username = form.cleaned_data.get('username')
			# password = form.cleaned_data.get('password1')
			# user = authenticate(username=username, password=password)
			# login(request, user)
			return redirect('activation_sent')
			# else:
			# form = SignUpForm()
			# messages.error(request,'username or password not correct')	
	else:
		form = SignUpForm()	
	return render(request, 'signup.html', {'form': form})

def activation_sent_view(request):
	return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	# checking if the user exists, if the token is valid.
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		# set signup_confirmation true
		user.profile.signup_confirmation = True
		user.save()
		login(request, user)
		return redirect('index')
	else:
		return render(request, 'activation_invalid.html')


def signin_view(request):
	if request.user.is_authenticated:
		return redirect('index')
	if (request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		if not username :
			messages.error(request,'username is empty',extra_tags='email')
		elif not password:
			messages.error(request,'password is empty')
		elif not User.objects.filter(username=username).exists():
			messages.error(request,'Username dose not exist')
		else:

			user = authenticate(request, username=username, password=password)
			if user is None:
				messages.error(request,'Username and password dose not match')
			elif not user.profile.signup_confirmation:
				messages.error(request,'Your account is not activate')
			else:
				login(request, user)
				return redirect('index')	
			
	return render(request, 'signin.html')

def logout(request):
	auth.logout(request)
	return redirect('index')		