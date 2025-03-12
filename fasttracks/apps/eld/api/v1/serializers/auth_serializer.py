from rest_framework import serializers
from .... import models


class VerificationCodeSerializer(serializers.Serializer):
    verification_code = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        fields = "__all__"

class CompanyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegisterCheck
        fields = ("first_name", "last_name", "email", "company_name", "usdot", "time_zone", "phone", "password")
