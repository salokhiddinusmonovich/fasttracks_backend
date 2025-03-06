from rest_framework import serializers
from .... import models






class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        exclude = ['id', 'image']