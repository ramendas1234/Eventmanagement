from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.html import mark_safe

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=200,default="")
	description = models.TextField(help_text="enter category description",default="")
	image = models.ImageField(upload_to='catalog/uploads', default="")
	def image_tag(self):
		return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.url))
	image_tag.short_description = 'Image'
	def __str__(self):
		return self.name


class Event(models.Model):
	title = models.CharField(max_length=300,  help_text="Enter event name",default="")
	description = models.TextField(blank=True,help_text="enter event description")
	publish_date = models.DateTimeField(default=datetime.now,editable=False)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, default=None, null=True)
	event_start_date = models.DateTimeField(default=datetime.now)
	event_end_date = models.DateTimeField(default=datetime.now)
	VENU_CHOICES = [
	('venue','Venue'),
	('online','Online')
	]
	event_venue = models.CharField(max_length=6,choices=VENU_CHOICES, default='online', null=True,blank=True)
	EVENT_TYPES = [
	('conference','Conference Of Convention'),
	('concert','Concert'),
	('seminar','Seminar Or Talk'),
	('festival','Festival Of Fair'),
	('performance', 'Performance Or Live Show'),
	('workshop','Class Training Or Workshop'),
	('networking','Meeting Or Networking Event'),
	('party','Party or Social Gathering'),
	('attraction','Attraction'),
	('appearance','Appearance Or Singing')
	]
	event_type = models.CharField(max_length=20,choices=EVENT_TYPES, default='conference', null=True,blank=True)
	event_location = models.TextField(max_length=500,  null=True,blank=True)
	city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True,blank=True)
	address = models.CharField(max_length=500,  null=True,blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	category = models.ManyToManyField(Category, help_text="Select category for this event")
	banner_image = models.ImageField(upload_to='catalog/uploads', default="")
	def banner_image_tag(self):
		print(self.banner_image.url)
		# pass
		return mark_safe('<img src="{0}" width="100%" height="300" />'.format(self.banner_image.url))
	thumb_image = models.ImageField(upload_to='catalog/uploads', default="")
	def thumb_image_tag(self):
		print(self.thumb_image.url)
		return mark_safe('<img src="{0}" width="300" height="300" />'.format(self.thumb_image.url))
	video_url = models.CharField(max_length=500 ,default="")
	website_link = models.CharField(max_length=300 ,default="")
	LISTING_TYPE = [
	('public', 'Public'),
	('private', 'Private'),
	]
	listing_type = models.CharField(max_length=10,choices=LISTING_TYPE, default='public')
	featured = models.BooleanField('make it features ? ',default=True)
	def __str__(self):
		return self.title



class Image(models.Model):
	event = models.ForeignKey(Event, related_name='images',on_delete=models.CASCADE)
	file = models.ImageField(upload_to='catalog/uploads')
	position = models.PositiveSmallIntegerField(default=0)

	class Meta:
		ordering = ['position']
	def __str__(self):
		return '{0} - {1} '.format(self.event, self.file)



class City(models.Model):
	name = models.CharField(max_length=300,  help_text="Enter city name",null=True,blank=True)
	def __str__(self):
		return self.name

class Tickit(models.Model):
	tickit_name = models.CharField(max_length=200, default="")
	tickit_quantity = models.CharField(max_length=10, default="")
	event = models.ForeignKey(Event,on_delete=models.CASCADE)
	TICKIT_TYPE = [('free','Free'),('paid','Paid')]
	tickit_type = models.CharField(max_length=5,choices=TICKIT_TYPE,default='free')
	CURRENCY_TYPE = [('inr','INR(₹)'),]
	payment_currency = models.CharField(max_length=20,choices=CURRENCY_TYPE,)
	tickit_price = models.CharField(max_length = 100, default="")
	PAYMENT_TYPE = [('online','Pay Online'),('venue','Pay at Venue')]
	payment_type = models.CharField(max_length=10,choices=PAYMENT_TYPE, default='online')
	def __str__(self):
		return self.tickit_name




