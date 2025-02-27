from django.urls import path

from fasttracks.apps.users.api.v1.views.user_views import (
    user_detail_api,
    user_redirect_api,
    user_update_api,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_api, name="redirect"),
    path("~update/", view=user_update_api, name="update"),
    path("<str:username>/", view=user_detail_api, name="detail"),
]
