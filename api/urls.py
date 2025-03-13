from django.urls import path, include

from api.spectacular.urls import urlpatterns as doc_urls
from fasttracks.apps.users.api.urls import urlpatterns as auth_urls
from fasttracks.apps.eld.api.urls import urlpatterns as eld_urls
# from api.front.urls import urlpatterns as front_api

app_name = 'api'

urlpatterns = []

urlpatterns += doc_urls
urlpatterns += auth_urls
urlpatterns += eld_urls

