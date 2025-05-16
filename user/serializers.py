from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


User  = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ['id','email','password','role','username']
      extra_kwargs = {
         'password' : {'write_only':True}
      }
    
    def create(self,validated_data):
       validated_data['password'] = make_password(validated_data['password'])
       return super().create(validated_data)
    
    def validate_role(self,value):
       valid_roles = ['admin','member']
       if value not in valid_roles:
          raise serializers.ValidationError("Role must be either admin or member")
       return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
    data = super().validate(attrs)
    user = self.user
    data['username'] = user.username
    data['email'] = user.email
    data['role'] = user.role
    return data

class MyTokenRefreshSerializer(TokenRefreshSerializer):
   def validate(self, attrs):
      data =  super().validate(attrs)
      refresh = RefreshToken(attrs["refresh"])
      user = User.objects.get(id = refresh["user_id"])
      data["email"] = user.email
      data["role"] = user.role
      data["username"] = getattr(user, "username", "")  
      return data




class SendOTPSerializer(serializers.Serializer):
   email = serializers.EmailField()