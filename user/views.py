from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random
from user.models import CustomUser, PasswordResetOTP
from .serializers import  MyTokenObtainPairSerializer, MyTokenRefreshSerializer, RegisterSerializer, ResetPasswordSerializer, SendOTPSerializer
from drf_yasg.utils import swagger_auto_schema
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi





@swagger_auto_schema(method='post', request_body=RegisterSerializer)
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status = status.HTTP_201_CREATED)
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='post', request_body=MyTokenObtainPairSerializer)    
@api_view(['POST'])
def login_view(request):
    serializer = MyTokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data)
    return Response(serializer.errors, status=400)

         
@swagger_auto_schema(method='post', request_body=MyTokenRefreshSerializer)    
@api_view(['POST'])
def refresh_token_view(request):
    serializer = MyTokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(method='post', request_body=SendOTPSerializer)    
@api_view(['POST'])
def send_otp_view(request):
    email = request.data.get("email")
    try:
        user = CustomUser.objects.get(email = email)
    except CustomUser.DoesNotExist:
        return Response({"message":"user not found"},status=status.HTTP_404_NOT_FOUND)
    otp=str(random.randint(100000,999999))
    expires_at = now() + timedelta(minutes=10)
    PasswordResetOTP.objects.create(user = user,otp = otp, expires_at = expires_at)
    send_mail(subject="Your Password Reset OTP",
              message=f"Your OTP is {otp}",
              from_email= "yaswanthsiddanatham264@gmail.com",
              recipient_list=[email]
              )
    return Response({'message':'OTP sent to email'},status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=ResetPasswordSerializer)
@api_view(['POST'])
def reset_password_view(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')
    try:
        user = CustomUser.objects.get(email = email)
    except CustomUser.DoesNotExist:
        return Response({"message":"User with this email not exists"},status=status.HTTP_404_NOT_FOUND)
    
    try:
        otp_obj = PasswordResetOTP.objects.filter(user = user,is_used = False,otp = otp,expires_at__gt = now()).latest('created_at')
    except PasswordResetOTP.DoesNotExist:
        return Response({"messgae":"Invalid or expired OTP"},status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    otp_obj.is_used = True
    otp_obj.save()
    return Response({"message":"Password reset successfully"},status=status.HTTP_200_OK)

    
