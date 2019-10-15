from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.core import serializers
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .serializers import *
from .models import *
from .forms import *
import datetime

def PersonCreateView(request):  
    form = PersonForm()
    return render(request,'person_form.html',{'form':form})

def person_list(request):
    name = request.POST.get('name')
    birthdate = request.POST.get('birthdate')
    country_id = request.POST.get('country')
    country=Country.objects.get(id=country_id)
    city_id = request.POST.get('city')
    city=City.objects.get(id=city_id)
   
    Person.objects.create(name=name,
        birthdate=datetime.datetime.strptime(birthdate, '%m/%d/%Y').strftime('%Y-%m-%d'),
        country=country,
        city=city)

    qs=Person.objects.all()
    ab=PersonSerializer(qs, many=True)
    return JsonResponse(ab.data, safe=False)


def person_list_ajax(request):
    persons=Person.objects.all()
    results = serializers.serialize('json', persons)
    data= json.loads(results)

    return HttpResponse(json.dumps(data))

def person_list_pagination(request):
    persons=Person.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(persons, 3)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'person_list.html',{'persons':persons,'users':users})

# For ajax use 

def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})