from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework import response
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




class RegisterFirstVersionAPI(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

   
    def send_to_email(self, email: str, model, count, time=datetime.now()):
        code = random.randint(100000, 999999)
        if count <= 3:
            send_mail(
                "Activation code",
                f"Your activation code is: {code}",
                "no-replay@gmail.com",
                [email],
                fail_silently=True
            )
            model.code = code
            model.email = email
            model.count = count + 1
            model.password = self.request.data.get("password")
            model.save()
            return response.Response({"data": {"status": "activation code has just been sent. "}})
        return response.Response({"status": "error", "couse": "please wait 5 minutes. "})
    
    
    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('email', openapi.IN_QUERY, description="User email", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('password', openapi.IN_QUERY, description="User password", type=openapi.TYPE_STRING, required=True),
    ],
    responses={200: "Activation code has been sent", 400: "Error response"},
    )


    # send email verification for company registration 
    def post(self, request):
        email = request.data.get("email")

        try:
            get_user_model().objects.get(email=email)
            return response.Response(
                {"data": {"status": "error", "couse": f"{email} already exists. "}}
            )
        except get_user_model().DoesNotExist:
            try:
                register_check = models.RegisterCheck.objects.get(email=email)
                time_now = datetime.now()
                times = register_check.time
                time_delta = timedelta(hours=times.hour, minutes=times.minute, seconds=times.second) - timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second)
                minutes = time_delta.total_seconds() // 60 
                if register_check.count >= 3:
                    if minutes >= 5:
                        count = 0
                        times = datetime.now()
                    else:count = register_check.count
                else: count = register_check.count
                    
                
                return self.send_to_email(
                    email=email, model=register_check, count=count, time=times
                )
            except Exception:
                return self.send_to_email(model=models.RegisterCheck(), email=email, count=0)


class CheckActiveationCodeFirstVersionAPI(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('email', openapi.IN_QUERY, description="User email", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('activation_code', openapi.IN_QUERY, description="Activation code", type=openapi.TYPE_INTEGER, required=True),
    ],
    responses={200: "User registered successfully", 400: "Error response"},
    )

    def post(self, request):
        try: value = models.RegisterCheck.objects.get(email=request.data["email"])
        except exceptions.ObjectDoesNotExist: return response.Response({"status": "error", "cause": "didn't send activation_code to email"})

        try:
            check_email = get_user_model().objects.get(email=request.data["email"])
            return response.Response({"data": {"status": "email duplicate"}})
        except exceptions.ObjectDoesNotExist: check_email = False

        if int(request.data["activation_code"]) == int(value.code):
            new_user = get_user_model(email=request.data["email"], password=make_password(value.password))
            new_user.save()

            # creating a new group
            new_user.groups.add("Comapny")

            serializer = auth_serializer.CompanySerializer(data=request.data)
            if serializer.is_valid():

                # saving Company and CustomUse
                send_mail(
                    "Thank you for registration",
                    "if you want more information you may visit Fasttracks.com/support",
                    "no-replay@gmail.com",
                    [request.data["email"]],
                    fail_silently=False, # stopping sending a message when error appears 
                )
            
                serializer.save()
            else: 
                return response.Response(serializer.errors)
            return response.Response({"data": serializer.data})
        return response.Response(
            {"data": {"status": "error", "cause": "activation code did not match."}}
        )
    
    
            
