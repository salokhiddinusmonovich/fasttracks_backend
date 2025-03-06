from django.urls import include, path

from fasttracks.apps.eld.api.v1.views import (
    auth_view
)

app_name = "eld"

company_url = [
    path("register/v1", auth_view.RegisterFirstVersionAPI.as_view()),
]



urlpatterns = [
    path("company/", include(company_url)),
]
