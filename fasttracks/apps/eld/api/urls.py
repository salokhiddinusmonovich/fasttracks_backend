from django.urls import include, path

from fasttracks.apps.eld.api.v1.views import (
    auth_view
)

app_name = "eld"

company_url = [
    path("register/", auth_view.RegisterAPI.as_view()),
    path('verify/', auth_view.VerifyAPI.as_view()),

]



urlpatterns = [
    path("company/", include(company_url)),
]
