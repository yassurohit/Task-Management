from django.urls import path
from .views import login_view, register_user, send_otp_view



urlpatterns = [
    path('register/',register_user,name= 'register'),
    path('login/', login_view, name='login'),
    path('send-otp/',send_otp_view,name='send-otp')
]