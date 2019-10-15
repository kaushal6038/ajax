from django.shortcuts import redirect, render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.http import JsonResponse,HttpResponse

from django.views.generic import (View,CreateView, DeleteView, DetailView, ListView,UpdateView)
from .models import *
from .forms import *

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class TeacherSignUpView(LoginRequiredMixin,View):
    login_url = 'login'
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'


    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                return render(request,self.template_name,{'form':form})
        else:
            return HttpResponse("user is not super")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            form = self.form_class(request.POST)
            return render(request,self.template_name,{'form':form})
        else:
            return HttpResponse("USer is Not superuser")
    # def get_context_data(self, **kwargs):
    #       kwargs['user_type'] = 'teacher'
    #      return super().get_context_data(**kwargs)

    # def form_check(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('/')

class StudentSignUpView(LoginRequiredMixin,View):
    login_url = 'login' 
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if self.request.user.is_superuser or self.request.user.is_teacher:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                return render(request,self.template_name,{'form':form})
        else:
            return HttpResponse("user is not Authorized")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_teacher:
            form = self.form_class(request.POST)
            return render(request,self.template_name,{'form':form})
        else:
            return HttpResponse("USer is Not Authorized")

