from django.urls import include, path

from fasttracks.apps.eld.api.v1.views import (
    auth_view,
    company_profile_view,
    drivers_view
)



app_name = "eld"

company_url = [
    path("register/", auth_view.RegisterAPI.as_view()),
    path('verify/', auth_view.VerifyAPI.as_view()),
    path('logout/', auth_view.LogoutAPI.as_view()),
    path("", company_profile_view.CompanyProfile.as_view())
    

]

drivers_url = [
    path("", drivers_view.DriversView.as_view())
]

urlpatterns = [
    path("company/", include(company_url)),
    path("drivers/", include(drivers_url)),
    
]
