from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from djongo.exceptions import SQLDecodeError
from .serializers import UserSerializer,LoginSerializer
from django.conf import settings
from .models import User
import random
import redis
import jwt
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)
from django.core.mail import send_mail


class register(GenericAPIView):
    serializer_class = UserSerializer
    def post(self,request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            user.is_active = False
            user_otp = random.randint(100000,999999)
            mess = f"Hello {user.username} your otp is :{user_otp}\nthanks"
            send_mail(
                "welcome to user registration",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
                      )
            redis_instance.set(user_otp,user.id)
            return Response({"User":"User created kindly check your mail for the OTP"},status=status.HTTP_201_CREATED)
        except SQLDecodeError as e:
            return Response({'DB_Connectivity':f'error fetching data from db due to {e}'})
        except Exception as err:
            return Response(err.__dict__,status=status.HTTP_400_BAD_REQUEST)


class verifyOTP(APIView):

    def post(self,request):
        otp=request.data.get('otp')
        try:
            value = redis_instance.get(otp)
            if not value:
                return Response({"OTP":"OTP is invalid or empty data"},status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.get(id=value)
                if not user.is_active:
                    user.is_active = True
                    user.save()
                redis_instance.delete(otp)
                return Response({'Message':'Successfully verified OTP'})
        except Exception as e:
            return Response({'error':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        try:
            data = request.data
            username=data.get('username','')
            password=data.get('password','')
            user = User.objects.get(username=username,password=password)

            if user:
                auth_token = jwt.encode({'username':user.username}, settings.SECRET_KEY, algorithm='HS256')
                redis_instance.set(user.id,auth_token)

                response =Response({'response':f'you are logged in successfully','username':user.username, 'token':auth_token},status=status.HTTP_200_OK)
                response['Authorization'] = auth_token
                return response
            return Response({'response':'Invalid credentials login again'},status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'response':'something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):

    def post(self,request):

        token = request.META.get('HTTP_TOKEN')
        print(token)
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,['HS256'])
            user = User.objects.get(username=payload['username'])
            value = redis_instance.get(user.id)

            if not value:
                return Response({'response':'failed to logout'},status=status.HTTP_400_BAD_REQUEST)
            else:
                result = redis_instance.delete(user.id)
                if result ==1:
                    return Response({'response':'Logged out successfully'},status=status.HTTP_200_OK)
                else:
                    return Response({'response':'failed to logout'},status=status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError as e:
            return Response({'response':'token expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'response':'invalid token'},status=status.HTTP_400_BAD_REQUEST)
