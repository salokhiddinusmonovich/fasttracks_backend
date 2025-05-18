from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from fasttracks.apps.eld import models
from ..serializers import serializers
from rest_framework.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class CompanyProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        if not request.user.is_authenticated:
            raise ValidationError("User is not authenticate.")
        
        try:
            return models.Company.objects.get(email=request.user.email)
        except models.Company.DoesNotExist:
            raise ValidationError("Company profile not found for the given user.")
        
    def clean_email(self, email):
        if email and (email[0] in ("'", '"')) and email[0] == email[-1]:
            email = email[1:-1]
        if models.Company.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
    
    def validate_password(self, old_password, new_password, user):

        if not user.check_password(old_password):
            raise ValidationError("The old pasword is incorrect!")
        
        if old_password == new_password:
            raise ValidationError("The new password cannot be the same as the old one.")
        
    def get(self, request):
        try:
            company_profile = self.get_object(request)
            return Response(serializers.CompanySerializer(company_profile).data)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="The new email of the user."),
                "old_password": openapi.Schema(type=openapi.TYPE_STRING, description="The user's current password."),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="The new password to be set."),
            },
            required=["old_password", "password"]
        ),
        responses={
            200: openapi.Response(description="Successfully updated the company profile."),
            400: openapi.Response(description="Invalid input, such as incorrect password or invalid email format."),
            403: openapi.Response(description="Permission denied. You do not have permission to access this resource."),
        }
    )
    def post(self, request):
        company_profile = self.get_object(request)
        user = request.user
        email = request.data.get("email")
        old_password = request.data.get("old_password")
        new_password = request.data.get("password")

        if email and email != user.email:
            user.email = self.clean_email(email)
        
        # Validate and change password if provided 
        if old_password and new_password:
            try:
                self.validate_password(old_password, new_password, user)
                user.set_password(new_password)
                user.save()
            except ValidationError as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializers.CompanySerializer(company_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyProfileImage(APIView):
    
    def get(self, request):
        try:
            company_profile = models.Company.objects.get(email=request.user.email)
            return Response({"image": company_profile.image.url}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "company does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        try:
            company_profile = models.Company.objects.get(email=request.user.email)
            company_profile.image = request.data.get("image", None)
            company_profile.save()
            return Response({"image": company_profile.image.url})
        except ObjectDoesNotExist:
            return Response({"message": "error"})