from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Event(models.Model):
	title = models.CharField(max_length=300,  help_text="Enter event name",null=True,blank=True)
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
	city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=500,  null=True,blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

class City(models.Model):
	name = models.CharField(max_length=300,  help_text="Enter city name",null=True,blank=True)
	def __str__(self):
		return self.name
class Category(models.Model):
	name = models.CharField(max_length=200,null=True)
	description = models.TextField(blank=True,help_text="enter category description")
	