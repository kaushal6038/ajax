from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.core import serializers
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test,login_required

from user.models import *
from .serializers import *
from .models import *
from .forms import *
import datetime

import csv


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def teachers(request):
    if request.user.is_teacher or request.user.is_superuser:
        teacher=Teacher.objects.all()
        return render(request,'teacher.html',{'teachers':teacher})
    else :
        return HttpResponse('User Is Not Authorized')

@login_required
def list_of_classes(request):
    classes = ClassesName.objects.all().order_by('name')
    return render(request,'classes.html',{'classes':classes})

def listOfStudents(request,pk):
    students = Student.objects.filter(Class=pk)
    return render(request,'student.html',{'students':students})

@login_required
@user_passes_test(lambda u: u.is_teacher or u.is_superuser)
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


def person_list(request):
    persons=Person.objects.all()
    return render(request,'list.html',{'personlist':persons})


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


def person_list_ajax(request):
    qs=Person.objects.all()
    ab=PersonSerializer(qs, many=True)  
    return JsonResponse(ab.data, safe=False)


# For ajax use 

def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})


def setsession(request):
    if request.user.is_teacher:
        request.session['name']='Kaushal'
        request.session['email']='kaushalk1003'
    else:
        request.session['name']='Empty'
        request.session['email']='empty value'

    return HttpResponse('session is set')

def getsession(request):
    name = request.session['name']
    email = request.session['email']
    return HttpResponse(name + ' ' + email)



from django.core.mail import send_mail
from django.conf import settings

def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['kaushalk1003@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return HttpResponse('succesfully send')


def classAdd(request):
    if request.method == "POST":
        form = classAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_signup')
    else:
        form=classAddForm()
    return render(request,'class_add.html',{'form':form})




from .resources import PersonResource

def csv_file(request):
    person_resource = PersonResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response 


from django.views.generic import View
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    # HTML(string=pdf_list).    write_pdf(result)

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def GeneratePDF(request):
    template = get_template('pdf_list.html')
    persons = Person.objects.all()
  
    html = template.render({'personlist':persons})
    pdf = render_to_pdf('pdf_list.html',{'personlist':persons})

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="persons.pdf"'
    return response

def GenerateDoc(request):
        template = get_template('pdf_list.html')
        persons = Person.objects.all()
        html = template.render({'personlist':persons})
        pdf = render_to_pdf('pdf_list.html',{'personlist':persons})
        response = HttpResponse(pdf, content_type='application/vnd.ms-word')
        response['Content-Disposition'] = 'attachment; filename="persons.doc"'
        return response