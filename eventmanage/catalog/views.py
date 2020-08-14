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
from .models import Event, City,Profile,Tickit, Category,Attendee,remove,is_username_use,is_email_use,handle_uploaded_file,get_total_price,home_url
from .forms import SignUpForm, ProfileImageUpload
import datetime
from django.db.models import Q
from django.contrib import auth

from django.contrib import messages
from django.contrib.auth.decorators import login_required

# 404 page
from django.shortcuts import render_to_response
from django.template import RequestContext

# Event Detail Page
from django.views import generic
from django.views.generic.list import ListView

# Event list category based list
from django.shortcuts import get_object_or_404

import re
import json
EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

#import our custom event library
from .event import EventLibrary

# Create your views here.



def index(request):
	now = datetime.datetime.now()
	featured_events = Event.objects.filter(Q(event_end_date__gt=now) & Q(listing_type='public') & Q(featured=True))
	performance_events = Event.objects.filter(Q(event_end_date__gt=now) & Q(listing_type='public') & Q(event_type='performance'))
	event_categories = Category.objects.all()
	data = { 'featured_events' : featured_events,'performance_events':performance_events,'categories':event_categories };
	return render(request, 'index.html',{'data':data})
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
		return render(request,'404.html')
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
		return render(request,'404.html')
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
				return redirect('/profile/update')	
			
	return render(request, 'signin.html')

def logout(request):
	auth.logout(request)
	return redirect('index')		

def view_dashboard(request, queryvar):
	print(queryvar)
	form = ProfileImageUpload()
	if not request.user.is_authenticated:
		return redirect('signin')

	profile = Profile.objects.get(user_id=request.user)
		
	if queryvar=='update':
		if request.method=='POST':
			data = {'flag':False, 'msg':''}
			first_name = remove(request.POST.get('first_name'))
			last_name = remove(request.POST.get('last_name'))
			username = remove(request.POST.get('username'))
			email = remove(request.POST.get('email'))
			CurrentUser = request.user
			if CurrentUser is None:
				data['msg'] = 'Please login and tray again'
			elif not len(first_name)>0:
				data['msg'] = 'Please enter first name'
			elif not len(last_name)>0:
				data['msg'] = 'Please enter last name'
			elif not len(username)>0:
				data['msg'] = 'Please enter user name'
			elif not is_username_use(username, CurrentUser.pk):
				data['msg'] = 'Sorry this username already use by another user'	
			elif not len(email)>0:
				data['msg'] = 'Please enter email'
			elif not re.match(EMAIL_REGEX, email):
				data['msg'] = 'Please enter a valid email'
			elif not is_email_use(email, CurrentUser.pk):
				data['msg'] = 'Sorry this email already use by another user'		
			else:
				CurrentUser.first_name = first_name
				CurrentUser.last_name = last_name
				CurrentUser.username = username
				CurrentUser.email = email
				CurrentUser.save()
				data['msg'] = 'Your profile update successfully'
				data['flag'] = True
			response = json.dumps(data)
			return HttpResponse(response)	
		else:	
			return render(request,'dashboard/account_update.html',{'form':form,'profile_image':profile.profile_image})

	if queryvar=='updateprofileimage':
		if request.method == 'POST':
			profile = Profile.objects.get(user_id=request.user)
			form = ProfileImageUpload(request.POST, request.FILES, instance=profile)

			if form.is_valid():
				profile = form.save()
		return render(request,'dashboard/account_update.html',{'form':form,'profile_image':profile.profile_image})
			
	return render(request,'404.html')


def dashboard(request):
	profile = Profile.objects.get(user_id=request.user)
	attendees = Attendee.objects.filter(Q(status=1)& Q(user_id=request.user))
	return render(request,'dashboard/dashboard.html',{'profile_image':profile.profile_image,'attendees':attendees})

class EventDetailView(generic.DetailView):
	model = Event
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['is_details'] = True
		context['similar_events'] = Event.objects.exclude(pk=self.object.pk)[:3]
		return context


class EventListView(ListView):
	model = Event
	# def get(self, request, *args, **kwargs):
	# 	print(self.kwargs['pk'])
	# 	return 'fdf'

	def get_queryset(self):
		catgId = self.kwargs['pk']
		return Event.objects.filter(category=catgId)
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		catgId = self.kwargs['pk']
		context['category'] = Category.objects.get(pk=catgId)
		return context	


def handler404(request, exception):
	print('404 --------')
	return render(request, '404.html', status=404)

# def handler500(request):
# 	print('500--------')
# 	return render(request, '404.html', status=500)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def attendee_process(request):
	data = {'flag':False, 'msg':''}
	if request.method=='POST':
		all_attendee = []
		attendee_name = request.POST.getlist('attendee_name[]')
		tickit_id = request.POST.getlist('tickit_id[]')
		attendee_email = request.POST.getlist('attendee_email[]')
		attendee_mobile = request.POST.getlist('attendee_mobile[]')
		
		for key, value in enumerate(attendee_name):
			#print(attendee_name[key],attendee_email[key],attendee_mobile[key])
			if attendee_name[key] == ''  or attendee_email[key] == '' or attendee_mobile[key] == '':
				data['msg'] = 'Please fill all fields'
				break
			else:
				all_attendee.append({'attendee_name':attendee_name[key], 'tickit_id':tickit_id[key], 'attendee_email':attendee_email[key],'attendee_mobile':attendee_mobile[key]})
		else:
			request.session['attendee_information'] = all_attendee
			data['flag'] = True

	response = json.dumps(data)	

	return HttpResponse(response)

def checkout_process(request):
	if not request.user.is_authenticated:
		return redirect('signin')
	attendees = request.session.get('attendee_information', '')
	# print(attendees)
	table_data = {}
	tickit_id = None
	cart_total = []
	total_price = 0
	total_qty = 0
	
	if len(attendees)>0:
		for item in attendees:
			if tickit_id == item.get('tickit_id',None):
				table_data[tickit_id] = table_data[tickit_id] + 1
			else:
				tickit_id = item.get('tickit_id',None)
				table_data[tickit_id] = 1

		for	item in table_data:
			cart_total.append({'tickit':Tickit.objects.get(pk=item),'qty':table_data[item]})
			total_price = total_price +  int(int(Tickit.objects.get(pk=item).tickit_price) * int(table_data[item]))
			total_qty = total_qty + int(table_data[item])
			
		
	# print(total_price)		
	return render(request,'checkout.html',{'data':attendees,'cart_data':cart_total,'total_price':total_price,'total_qty':total_qty})

# payment regarding


import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
# payment process is done here
def payment_render(request):
	attendees = request.session.get('attendee_information', '')
	ids = ''
	# Insert attendee data to model
	for item in  attendees:
		tickit = Tickit.objects.get(pk=item['tickit_id'])
		attendee = Attendee(attedee_name=item['attendee_name'],attendee_email=item['attendee_email'],attendee_mobile=item['attendee_mobile'],event_id=tickit.event_id,tickit_id=item['tickit_id'],user_id=request.user.id)
		attendee.save()
		ids = ids + str(attendee.id) + ','

	MERCHANT_KEY = "Ijuab2G7"
	key="Ijuab2G7"
	SALT = "BooAHiDslz"
	PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
	action = ''
	price = get_total_price(attendees)
	attendees = str(attendees)
	posted={
		'key' : MERCHANT_KEY,
		'hash_string': '',
		'hash' : '',
		'txnid' : '',
		'amount' : price,
		'firstname' : request.user.username,
		'email' : request.user.email,
		'productinfo' : 'product info',
		'udf1' : ids[:-1],
		'surl' : home_url()+'/success/',
		'furl' : home_url()+'/failure/',
		'service_provider':'payu_paisa',

	}
	hash_object = hashlib.sha256(b'randint(0,20)')
	txnid=hash_object.hexdigest()[0:20]
	hashh = ''
	posted['txnid']=txnid
	hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
	hash_string=''
	hashVarsSeq=hashSequence.split('|')
	for i in hashVarsSeq:
		try:
			hash_string+=str(posted[i])
		except Exception:
			hash_string+=''
		hash_string+='|'
	hash_string+=SALT
	# print('-------------------',hash_string)
	hash_string = hash_string.encode('utf-8')
	hashh=hashlib.sha512(hash_string).hexdigest().lower()
	# print('----------after encode---------',hash_string)
	posted['hash'] = hashh
	posted['hash_string'] = hash_string

	return render(request,'payu.html',{'action':PAYU_BASE_URL,'param_dict':posted})

@csrf_protect
@csrf_exempt
# @login_required
def success(request):
	c = {}
	print('This is user',request.user)
	# c.update(csrf(request))
	attendees = request.session.get('attendee_information', '')
	
	if request.method == "POST":
		ids = request.POST["udf1"].split(',')
		status=request.POST["status"]
		firstname=request.POST["firstname"]
		amount=request.POST["amount"]
		txnid=request.POST["txnid"]
		posted_hash=request.POST["hash"]
		key=request.POST["key"]
		productinfo=request.POST["productinfo"]
		email=request.POST["email"]
		udf1 = request.POST["udf1"]
		salt="BooAHiDslz"
		try:
			additionalCharges=request.POST["additionalCharges"]
			retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
		except Exception:
			retHashSeq = salt+'|'+status+'||||||||||'+udf1+'|'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
		retHashSeq = retHashSeq.encode('utf-8')
		hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
		'''print('hashh value: ',hashh)
		print('posted  value: ',posted_hash)
		print('UDF1 :', ids)
		exit()'''
		if(hashh !=posted_hash):
			for item in ids:
				attendeeObj = Attendee.objects.get(pk=item)
				attendeeObj.delete()
			print("Invalid Transaction. Please try again")
			return render(request,"Failure.html")
		else:
			for item in ids:
				attendeeObj = Attendee.objects.get(pk=int(item))
				attendeeObj.status = True
				attendeeObj.save()
			# send mail after attendee complete
			current_site = get_current_site(request)
			subject = 'Your attendee booking successfully'
			message = render_to_string('attendee_email.html', {
			'amount': amount,
			'domain': current_site.domain,
			})
			send_mail(subject,message, 'ramend3@gmail.com',['to@example.com'])	
			'''print('------attendee--------',attendees)
			print('------product info success------',productinfo)
			print("Thank You. Your order status is ", status)
			print("Your Transaction ID for this transaction is ",txnid)
			print("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")'''
			return render(request,'sucess.html',{"txnid":txnid,"status":status,"amount":amount})

	
	return HttpResponse('not allowed this page')	


from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail

@csrf_protect
@csrf_exempt
# @login_required
# @require_http_methods(["POST"])

def failure(request):
	
	if request.method=='POST':
		ids = request.POST["udf1"].split(',')
		for item in ids:
			print(item)
			attendeeObj = Attendee.objects.get(pk=item)
			attendeeObj.delete()
		return render(request,"Failure.html")
		
	return HttpResponse('not allowed this page')	






def test(request,pk):
	print('PK',pk)
	# dict_test = {'name1':'Ramen','name2':'Pritam'}
	# request.session['my_car'] = dict_test
	# print(request.session['my_car'])
	return render(request,"sucess.html")
	

	
	
	# Delete a session value
	#del request.session['my_car']

	"""if request.method == 'POST':
		files = request.FILES
		print(files)

		
		profile = Profile.objects.get(user_id=request.user)
		print('current user------', request.user)
		print('Profile -----------', profile)
		print(profile.first_name)
		print(profile.last_name)
		form = ProfileImageUpload(request.POST, request.FILES, instance=profile)
		print(form)
		if form.is_valid():
			profile = form.save()
			

		else:
			print(form.errors)	"""
		# files = request.FILES
		# attached_file1 = files.get('file1', None)
		# handle_uploaded_file(attached_file1)
		# print(attached_file1)
		# full_filename = '/media/'+'catalog/uploads'+attached_file1
		
	return HttpResponse('testing')