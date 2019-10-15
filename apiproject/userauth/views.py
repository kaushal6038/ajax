from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.response import Response
from .serializers import *
from django.shortcuts import redirect,HttpResponse,render
from django.conf import settings
from .forms import EmailForm,OtpForm
# APi Response
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

# Api Views
from rest_framework import generics
from rest_framework.views import APIView

from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User

# Twillio
from twilio.rest import Client

# for Otp
import math,random
from datetime import datetime, timedelta 

# Raising Error or Success Messages
from django.contrib import messages

# For sending Email
from django.core.mail import send_mail


# Twillio user details
account_sid = 'ACd2039c60cce1e64ca94fd8817c3d04ff'
auth_token = '6cc79b6371de7a16b64953feef11efa0'
client = Client(account_sid, auth_token)




class UserListView(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = CustomUser.objects.all()
	serializer_class = UserSerializer


def otp():

	digits = "0123456789"
	OTP = ""
	for i in range(6) : 
		OTP += digits[math.floor(random.random() * 10)] 
	return OTP 


# For Api Email Validation --------------------------------------------------

class EmailView(APIView):

	def get(self,request):
		usernames = [user.email for user in UserOtp.objects.all()]
		serializer = OtpSerializer()
		return Response({'User':usernames,'serializer':serializer.data})

	def post(self,request):
		
		serializer=OtpSerializer(data=request.data)
		
		if serializer.is_valid():
			request.session['email']=(serializer.data['email'])
			usernames = [user.email for user in UserOtp.objects.all()]

			registered_emails=[user.email for user in CustomUser.objects.all()]
			
			if request.session['email'] in registered_emails :
			
				request.session['otp']= otp()
				request.session['time']=str(datetime.now().strftime("%m/%d/%y %H:%M:%S"))
				
				subject = 'Thank you for registering to our site'
				message = 'Your required Otp is '+ request.session['otp']
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [request.session['email'],]
				send_mail( subject, message, email_from, recipient_list )
				
				messages.success(request,('OTP has been Send to your defined email address'))
				return HttpResponseRedirect(redirect_to='otpval')

			else:
			
				return HttpResponseRedirect(redirect_to='/api/v1/auth/registration/')				
		return  Response({'message': 'Please Check Your Email Address'})

class OtpValidate(APIView):

	def get(self,request):
		email = request.session['email']
		return Response({'email':email,})

	def post(self,request):
		email = request.session['email']
		otp_time = datetime.strptime(request.session['time'],'%m/%d/%y %H:%M:%S')

		otp_duration = otp_time + timedelta(minutes = 1)

		current_time=datetime.now().strftime("%m/%d/%y %H:%M:%S")
		current_time=datetime.strptime(current_time,'%m/%d/%y %H:%M:%S')	
			
		emailreq=request.data

		serializer = OtpValidateSerializer(data=request.data)
		if serializer.is_valid():

			if (serializer.validated_data.get('email')==request.session['email']) and\
			(int(serializer.validated_data.get('otp'))==int(request.session['otp'])):

				if current_time >= otp_duration:
					return Response({'message': 'OTP Expired'})
				else :
					registered_emails=[user.email for user in CustomUser.objects.all()]
					user=CustomUser.objects.get(email=email)

					if user:
						print(user)
						login(request,user)
					
						return Response({"message":"user is authenticated"})
			else:
				return Response({'message': 'Invalid OTP'})
		return Response({'message': 'please check the OTP'}) 


def phoneOtp(request):
	message = client.messages \
	.create(
	     body='This is the ship that made the Kessel Run in fourteen parsecs?',
	     from_='whatsapp:+14155238886',
	     to='whatsapp:+917206760665'
	 )
	print(message.sid)
	print(message.status)
	return HttpResponse("mesage is send")


# For Django email and OTp validation ------------------------------------------------------------

# def emailOtp(request):
# 	if request.method == "POST":

# 		form=EmailForm(request.POST)
		
# 		if form.is_valid():
# 			# request.session['email']=(form.cleaned_data['email'])
# 			# registered_emails =[user.email for user in CustomUser.objects.all()]
# 			# if request.session['email'] in registered_emails :
			
# 			# 	request.session['otp']= otp()
# 			# 	request.session['time']=str(datetime.now().strftime("%m/%d/%y %H:%M:%S"))
				
# 			# 	subject = 'Thank you for registering to our site'
# 			# 	message = 'Your required Otp is '+ request.session['otp']
# 			# 	email_from = settings.EMAIL_HOST_USER
# 			# 	recipient_list = [request.session['email'],]
# 			# 	send_mail( subject, message, email_from, recipient_list )
# 			# 	print(True)
# 			# 	return redirect('emailotpval/')
# 			return HttpResponse("Email is not registered with us")	
# 	else:
# 		form=EmailForm()
# 		formotp = OtpForm()
# 		return render(request,'email.html',{'form':form,'fromotp':formotp})

def emailOtp(request):
	if request.method == "POST":
		otp_time = datetime.strptime(request.session['time'],'%m/%d/%y %H:%M:%S')

		otp_duration = otp_time + timedelta(minutes = 1)

		current_time=datetime.now().strftime("%m/%d/%y %H:%M:%S")
		current_time=datetime.strptime(current_time,'%m/%d/%y %H:%M:%S')	
			
		

		form = OtpForm(request.POST)

		if form.is_valid():

			if (form.cleaned_data['email']==request.session['email']) and\
			 (int(form.cleaned_data['otp'])==int(request.session['otp'])):

				if current_time >= otp_duration:
					return HttpResponse('OTP Expired')
				else :
					registered_emails=[user.email for user in CustomUser.objects.all()]
					user=CustomUser.objects.get(email=request.session['email'])

					if user:
						print(user)
						login(request,user)
					
						return redirect('/admin')
			else:
				messages.error(request, "Invalid OTP")
				return JsonResponse({'message':'Invalid OTP'})
			# return HttpResponse( 'please check the OTP')
			return render(request,'email.html',{'form':form})
	else:
		form = OtpForm(request.POST)
		return render(request,'email.html',{'form':form})


# Email and Otp validation using AJAX ------------------------------------------------------------

def emailAjax(request):
	email=request.POST.get('email')
	request.session['email']=email
	registered_emails =[user.email for user in CustomUser.objects.all()]
	
	if request.session['email'] in registered_emails :
		request.session['otp']= otp()
		request.session['time']=str(datetime.now().strftime("%m/%d/%y %H:%M:%S"))
		
		subject = 'Thank you for registering to our site'
		message = 'Your required Otp is '+ request.session['otp']
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [request.session['email'],]
		send_mail( subject, message, email_from, recipient_list )

		return JsonResponse({'status':'True'}, status=200)
	return JsonResponse({'status':'False','message':'Your Account is Not Regiistered with us'},status=200)
	
def emailValAjax(request):
	email = request.POST.get('email')
	otp = request.POST.get('otp')

	otp_time = datetime.strptime(request.session['time'],'%m/%d/%y %H:%M:%S')
	otp_duration = otp_time + timedelta(minutes = 1)
	current_time=datetime.now().strftime("%m/%d/%y %H:%M:%S")
	current_time=datetime.strptime(current_time,'%m/%d/%y %H:%M:%S')
	print(otp)
	print(email)
	if (email == request.session['email']) and\
		(int(otp)==int(request.session['otp'])):
		if current_time >= otp_duration:
			return JsonResponse({'status':'expired'}, status=200)
		else:
			registered_emails=[user.email for user in CustomUser.objects.all()]
			user=CustomUser.objects.get(email=request.session['email'])

			if user:
				print(user)
				login(request,user)

				return JsonResponse({'status':'True'}, status=200)
	return JsonResponse({'status':'False'}, status=200)



















# class EmailView(generics.ListCreateAPIView):
# 	queryset = User.objects.all()
# 	serializer_class = OtpSerializer



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# import random as r


# def otpgen():
# 	otp=""
# 	for i in range(6):
# 		otp+=str(r.randint(1,9))
# 	return otp


# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)



