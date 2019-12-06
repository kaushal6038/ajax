from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.
from .models import Location 
from django.contrib.gis.geos import Point #GeoDjango takes lat and lng values in Point object.
from .forms import PersonForm
from django.contrib.gis.measure import Distance  

from opencage.geocoder import OpenCageGeocode

from django.core import serializers
import json

key = '3be6eb6287214324b7bcd2e4df98890e'
geocoder = OpenCageGeocode(key)


def details(request):
	form = PersonForm()
	return render(request,'data.html',{'form':form})

def current_location(request):
	name= request.POST.get('name')
	address= request.POST.get('address')
	longitude = request.POST.get('longitude')
	latitude = request.POST.get('latitude')
	longitude,latitude=float(longitude),float(latitude)
	location_point=Point(longitude,latitude)

	if Location.objects.filter(name=name,geo_location=location_point):
		return JsonResponse({'message':'user already registered'})
	else:
		Location.objects.create(name=name,address=address,geo_location=location_point)
	return JsonResponse({'message':"Success"})

def buyer_location(request):
	longitude = 76.702074
	latitude = 30.715480
	g = geocoder.reverse_geocode(latitude, longitude)
	x=g[0]['formatted'].split(',')
	print(x[0])
	return render(request,'user.html')

def nearest_stores(request):
	longitude = float(request.POST.get('longitude'))
	latitude =	float(request.POST.get('latitude'))
	longitude = 76.702074
	latitude = 30.715480


	location_point=Point(longitude,latitude)
	radius=5
	
	shops=Location.objects.filter(geo_location__distance_lt=(location_point, Distance(km=radius)))
	
	results = serializers.serialize('json', shops)
	data= json.loads(results)

	x=[shop.geo_location.x for shop in shops]
	y=[shop.geo_location.y for shop in shops]
	mapbox_access_token = 'pk.eyJ1Ijoia2F1c2hhbDE3NyIsImEiOiJjazJlbDZseHUwNjNhM2xwdGgxeWZjNXNxIn0.nuPmPOZP5jRSy6LP4XP3gg';
	print(x[0])

	location=[]
	for i in range(len(x)):
		g = geocoder.reverse_geocode(y[i], x[i])
		location1=g[0]['formatted'].split(',')
		print(location1[0])
		location.append(location1[0])

	print(location)

	return JsonResponse({'longitude':longitude,'latitude':latitude,\
			'mapbox_access_token': mapbox_access_token,"x":x,'y':y,\
			'shops':data,'location':location})

def stores_list(request):
	return render(request,'store_list.html')
	
