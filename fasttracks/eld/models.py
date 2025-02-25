from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()




class Company(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=100, unique=True)
    usdot = models.IntegerField()
    time_zone = models.CharField(max_length=500)
    phone = models.CharField(max_length=100)
    image = models.ImageField(upload_to='company_image/')
    address = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True, max_length=15)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_name} & {self.email}"

    class Meta:
        verbose_name_plural = "Companies"


class ELD(models.Model):
    serial_number = models.CharField(max_length=30)
    notes_eld = models.CharField(blank=True, null=True, default="", max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    objects = VehicleManager()

    def __str__(self):
        return self.serial_number


class Vehicle(models.Model):
    vehicle_id = models.CharField(unique=True, max_length=200)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.IntegerField()
    license_plate_num = models.CharField(
        unique=True, max_length=500, null=True, blank=True
    )
    license_plate_issue_state = models.CharField(max_length=100)
    vin = models.CharField(blank=True, max_length=30, null=True)
    eld_id = models.OneToOneField(ELD, on_delete=models.CASCADE, null=True)
    notes_vehicle = models.CharField(blank=True, null=True, default="", max_length=200)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    activate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    device_version = models.CharField(max_length=500, blank=True, null=True)
    status = models.BooleanField(default=True)
    fuel_type = models.CharField(max_length=200, null=True, blank=True)
    objects = VehicleManager()
    terminated = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.model} - {self.vehicle_id}"


class Trailer(models.Model):
    trailer_number = models.CharField(max_length=50)
    company = models.ForeignKey(Company, models.CASCADE)

    def __str__(self):
        return self.trailer_number


class Notes(models.Model):
    text = models.TextField()
    driver = models.ForeignKey("DRIVERS", models.CASCADE)


class DRIVERS(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='company_image/')
    phone = models.CharField(max_length=30)
    driver_license_number = models.CharField(max_length=250)
    dr_li_issue_state = models.CharField(max_length=100)
    co_driver = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )
    home_terminal_address = models.CharField(max_length=200, null=True, blank=True)
    home_terminal_time_zone = models.CharField(max_length=200)
    vehicle_id = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
    )
    status = models.BooleanField(default=True)
    trail_number = models.ManyToManyField(Trailer, blank=True, null=True)
    enable_dr_eld = models.BooleanField(default=False)
    enable_dr_elog = models.BooleanField(default=False)
    allow_yard = models.BooleanField(default=False)
    allow_personal_c = models.BooleanField(default=False)
    enable_ssb = models.BooleanField(default=False)
    enable_short_haul = models.BooleanField(default=False)
    adverse_driving_conditions = models.BooleanField(default=False)
    disable_correction = models.BooleanField(default=False)
    color = models.CharField(max_length=50, blank=True, null=True,default='')
    activated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    terminated = models.DateTimeField(default=None,blank=True, null=True)
    app_version = models.CharField(max_length=200, blank=True, null=True)
    device_version = models.CharField(max_length=500, blank=True, null=True)
    main_office = models.CharField(max_length=700, null=True)
    company = models.ForeignKey("Company", models.CASCADE)
    address1 = models.CharField(max_length=255, default='')
    address2 = models.CharField(max_length=255, null=True, blank=True, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    zip = models.CharField(max_length=20, default='')
    objects = VehicleManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Drivers"


class EventDriver(models.Model):
    engine_state = models.CharField(max_length=45, null=True, blank=True)
    vin = models.CharField(max_length=50, null=True, blank=True)
    speed_kmh = models.CharField(max_length=50, null=True, blank=True)
    odometer_km = models.CharField(max_length=50, null=True, blank=True)
    trip_distance_km = models.CharField(max_length=50, null=True, blank=True)
    hours = models.CharField(max_length=50, null=True, blank=True)
    trip_hours = models.CharField(max_length=50)
    voltage = models.CharField(max_length=50)
    date = models.DateTimeField()
    time = models.DateTimeField()
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    gps_speed_kmh = models.CharField(max_length=50)
    course_deg = models.CharField(max_length=50)
    namsats = models.CharField(max_length=50)
    altitude = models.CharField(max_length=50)
    drop = models.CharField(max_length=50)
    sequence = models.CharField(max_length=50)
    firmware = models.CharField(max_length=50)
    driver = models.ForeignKey("DRIVERS", on_delete=models.CASCADE)

    def __str__(self):
        return self.driver


class RegisterCheck(models.Model):
    email = models.EmailField(unique=True, blank=True, null=True)
    time = models.TimeField(default=None, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=150, blank=True, null=True)
    count = models.IntegerField(default=0)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    usdot = models.IntegerField(blank=True, null=True)
    time_zone = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
