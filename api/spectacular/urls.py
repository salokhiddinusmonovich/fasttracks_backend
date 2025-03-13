# region --------  Old code ---------
# from django.urls import path
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework import permissions
#
# schema_view = get_schema_view(
#    openapi.Info(
#       title="Fasttracks API",
#       default_version='v1',
#       description="Fasttracks project apis",
#       contact=openapi.Contact(email="usmonovsalokhiddin@gmail.com"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )
#
#
# urlpatterns = [
#     path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]
#endregion ----------------

from django.urls import path

from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]