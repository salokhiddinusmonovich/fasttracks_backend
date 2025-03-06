from django.contrib import admin
from .models import Company, ELD, Vehicle, Trailer, Notes, DRIVERS, EventDriver, RegisterCheck

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("company_name", "email", "phone", "is_active")
    search_fields = ("company_name", "email")

@admin.register(ELD)
class ELDAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "company", "status", "version")
    search_fields = ("serial_number", "company__company_name")

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("vehicle_id", "model", "company", "status")
    search_fields = ("vehicle_id", "model", "company__company_name")

@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ("trailer_number", "company")
    search_fields = ("trailer_number", "company__company_name")

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ("driver", "text")
    search_fields = ("driver__name", "text")

@admin.register(DRIVERS)
class DriversAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "company")
    search_fields = ("name", "email", "company__company_name")

@admin.register(EventDriver)
class EventDriverAdmin(admin.ModelAdmin):
    list_display = ("driver", "date", "time", "latitude", "longitude")
    search_fields = ("driver__name", "date")

@admin.register(RegisterCheck)
class RegisterCheckAdmin(admin.ModelAdmin):
    list_display = ("email", "company_name", "time", "count")
    search_fields = ("email", "company_name")
