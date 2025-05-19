from django.urls import path
from .views import login_view, register_user, reset_password_view, send_otp_view



urlpatterns = [
    path('register/',register_user,name= 'register'),
    path('login/', login_view, name='login'),
    path('send-otp/',send_otp_view,name='send-otp'),
    path('reset-password',reset_password_view,name = 'reset-password'),
]