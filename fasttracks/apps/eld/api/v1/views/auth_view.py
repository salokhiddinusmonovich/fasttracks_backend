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



class RegisterFirstVersionAPI(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

   
    def send_to_email(self, email: str, model, count, time=datetime.now()):
        code = tools.confirmation_code_generator()
        if count <= 3:
            if settings.DEBUG:
                send_mail(
                    "Activation code",
                    f"Your activation code is: {code}",
                    "no-replay@gmail.com",
                    [email],
                    fail_silently=False
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
            openapi.Parameter(
                'email', openapi.IN_QUERY, description="User email", type=openapi.TYPE_STRING, required=True
            ),
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
                return self.send_to_email(model=models.RegisterCheck(), email=email, count=count)