from django.urls import path

from fasttracks.apps.users.api.v1.views.auth_views import CustomTokenObtainPairView, CustomTokenVerifyView, \
    CustomTokenRefreshView
from fasttracks.apps.users.api.v1.views.user_views import (
    user_detail_api,
    user_redirect_api,
    user_update_api,
)

app_name = "users"
urlpatterns = [
    path("redirect/", view=user_redirect_api, name="redirect"),
    path("update/", view=user_update_api, name="update"),
    path("<str:email>/", view=user_detail_api, name="detail-by-email"),
    path('auth/jwt/create', CustomTokenObtainPairView.as_view(), name='create-token'),
    path('auth/jwt/refresh', CustomTokenRefreshView.as_view(), name='refresh-token'),
    path('auth/jwt/verify', CustomTokenVerifyView.as_view(), name='verify-token'),
]
