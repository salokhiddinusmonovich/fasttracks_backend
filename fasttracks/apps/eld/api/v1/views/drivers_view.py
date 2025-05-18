from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_list_or_404
from fasttracks.apps.eld import models
from rest_framework import status
from fasttracks.apps.eld.api.v1.serializers import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

def default_user_authentication_rule(user):
    if models.DRIVERS.objects.filter(email=user.email).exists():
        driver = models.DRIVERS.objects.get(email=user.user)
        return user is not None and driver.status
    else:
        return user is not None and user.is_active
    


class DriversView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = models.DRIVERS.objects.all()

    def get(self, request):
        user = request.user

        try:
            drivers = models.DRIVERS.for_company_manager.for_company(user=user)
            vehicles = models.Vehicle.for_company_manager.for_company(user=user)

            if drivers is None or vehicles is None:
                return Response({"error": "Failed to fetch drivers or vehicles"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            reserved_vehicl_ids = drivers.values_list("vehicle_id__vehicle_id", flat=True).distinct()

            total_vehicle_ids = {vehicle.id: vehicle.vehicle_id for vehicle in vehicles}

            available_vehicle_ids = [vehicle_id for vehicle_id in total_vehicle_ids.values() if vehicle_id not in reserved_vehicl_ids]


            if not drivers:
                context = {
                    "data": {
                        "status": "empty",
                        "available_vehicle_id": available_vehicle_ids
                    }
                }
            
            serializer = serializers.DriverSerializer(drivers, many=True)
            context =  {
                "data": {
                    "drivers": serializer.data,
                    "available_vehicle_id": available_vehicle_ids
                }
            }

            return Response(context)
        
        except models.DRIVERS.DoesNotExist:
            return Response({"error": "DRIVERS object does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except models.Vehicle.DoesNotExist:
            return Response({"error": "Vehicle object does not exsit"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
