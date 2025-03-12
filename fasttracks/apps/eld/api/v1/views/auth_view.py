from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from fasttracks.apps.eld import models
from django.core import exceptions
from rest_framework import views
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from ..services import tools
from django.conf import settings
from django.core.mail import send_mail
from ..services import query_params
from ...v1.serializers import auth_serializer
import random




class RegisterAPI(GenericAPIView):
    serializer_class = auth_serializer.CompanyRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = self.request.data

        try:
            get_user_model().objects.get(email=data.get("email"))
            models.Company.objects.get(email=data.get("email"))
            return Response({
                "status": "error", "message": "this email is registered."
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        try:
            check_register = models.RegisterCheck.objects.create(**data)
            code = tools.send_verification_code_to_email__second_version(email=check_register.email)
            check_register.code = code 
            check_register.save()
            response_token = tools.encode_email(email=check_register.email)
            return Response({"token": response_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyAPI(GenericAPIView):
    serializer_class = auth_serializer.VerificationCodeSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(manual_parameters=query_params.get_token())
    def post(self, request):
        token = self.request.query_params.get("token")
        email = tools.decode_email(token)
        code = self.request.data.get("verification_code")
        try:
            not_auth_company = models.RegisterCheck.objects.get(email=email)
            if not_auth_company.code == int(code):
                user = get_user_model().objects.create(email=not_auth_company.email, 
                                                       password=not_auth_company.password,
                                                       first_name=not_auth_company.first_name, 
                                                       last_name=not_auth_company.last_name,
                                                       is_active=True
                                                       )
                user.set_password(not_auth_company.password)
                user.save()
                models.Company.objects.create(first_name=not_auth_company.first_name, 
                                              last_name=not_auth_company.last_name,
                                              email=not_auth_company.email,
                                              company_name=not_auth_company.company_name,
                                              usdot=not_auth_company.usdot,
                                              time_zone=not_auth_company.time_zone,
                                              phone=not_auth_company.phone
                                              )
                return Response({"message": "successfully registered."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)