from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [

    # Django Admin, use {% url 'admin:index' %}
    path("system/admin/panel/", admin.site.urls),
    path('api/', include('api.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path("", TemplateView.as_view(template_name="pages/logistic.html"), name="home"),

]

