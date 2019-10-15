from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.UserListView.as_view(),name='users'),
    path('otp',views.EmailView.as_view()),
    path('otpval',views.OtpValidate.as_view(),name='OtpValidate'),
    path('phone',views.phoneOtp),
    path('otpemail',views.emailOtp),
    # path('emailotpval/',views.emailOtpValidate),
    path('email-ajax',views.emailAjax),
    path('email-val-ajax',views.emailValAjax),
]