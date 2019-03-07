from django.urls import path

from . import views

urlpatterns = [
    path('agent-signup/', views.AgentSignUpAPIView.as_view()),
    path('owner-signup/', views.PropertyOwnerSignUpAPIView.as_view()),
    path('government-signup/', views.GovernmentSignUpAPIView.as_view()),
    path('hotel-signup/', views.HotelierSignUpAPIView.as_view()),
    path('customer-signup/', views.CustomerSignUpAPIView.as_view(), name='customer'),
    path('supplier-signup/', views.SupplierSignUpAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('developer-signup/', views.DeveloperSignUpAPIView.as_view()),
    path('valuer-signup/', views.ValuerSignUpAPIView.as_view()),
    path('institute-signup/', views.InstituteSignUpAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('confirm-number/', views.ValidateNumberAPIView.as_view()),
    path('resend-otp/', views.ResendOTPAPIView.as_view(), name='resend-otp'),
    path('resend-email-code/', views.ResendEmailCodeAPIView.as_view()),
    path('reset-password/number/', views.PasswordResetNumberAPIView.as_view()),
    path('reset-password/email/', views.PasswordRestEmailAPIView.as_view()),
    path('reset-password/confirm-code/', views.PasswordResetOTPConfirmedAPIView.as_view()),
    path('reset-password/confirm-email-code/', views.ConfirmedEmailCodeAPIView.as_view()),
    path('reset-password/confirm/', views.PasswordResetConfirmAPIView.as_view()),
    path('resend-otp-code/', views.ResendOTPTokenView.as_view()),
    path('reconfirm-number/', views.ReconfirmAccountNumberAPIView.as_view()),
    path('confirm-code/', views.ReconfirmAccountNumberValidationAPIView.as_view()),
    path('send-auth-code/', views.VerificationAPIView.as_view())
    ]