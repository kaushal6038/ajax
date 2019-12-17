from django.shortcuts import render
from .models import *
# Create your views here.

def test(request):
	data = Modeltest.objects.all()
	return render(request, 'test.html' ,{'data':data})

def user_list(request):
    return render(request, 'user_list.html')