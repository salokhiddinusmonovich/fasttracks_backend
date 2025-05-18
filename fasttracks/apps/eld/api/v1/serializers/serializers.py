from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .... import models
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from rest_framework import serializers



User = get_user_model()


class EldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ELD
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vehicle
        fields = '__all__'

class VehicleSerializerTerminated(serializers.ModelSerializer):
    class Meta:
        model = models.Vehicle
        exclude = ['terminated']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DRIVERS
        exclude = ['password', 'terminated']



class DriverSerializer2(serializers.ModelSerializer):
    class Meta:
        model = models.DRIVERS
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventDriver
        fields = ['engine_state', 'vin', 'rpm', 'speed_kmh', 'odometr_km', 'trip_distance_km', 'hours',
                  'trip_hours', 'voltage', 'date',
                  'time', 'latitude', 'longitude', 'gps_speed_kmh', 'course_deg', 'namsats', 'altitude',
                  'drop', 'sequence', 'firmware', "driver"]

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        exclude = ['id']