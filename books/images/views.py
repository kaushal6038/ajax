from django.shortcuts import render,redirect
from django.conf import settings
from django.views import View
from django.http import JsonResponse
import time

from django.core.files.storage import FileSystemStorage

from .models import *
from .forms import *


def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        
        return render(request, 'simple_upload.html',
                {'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')


class model_form_upload(View):
    def get(self,request):
        photos = Photo.objects.all()
        return render(request,'model_form_upload.html',{'photos':photos})

    def post(self,request):
        time.sleep(1) 
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo=form.save()
            data={'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False }
        return JsonResponse(data)

def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'model_form_upload.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)