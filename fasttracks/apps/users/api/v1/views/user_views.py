from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from fasttracks.apps.users.api.v1.serializers.user_serializers import UserSerializer


User = get_user_model()


class UserDetailAPI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "email"
    permission_classes = [permissions.IsAuthenticated]



class UserUpdatedAPI(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserRedirectAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        url = reverse("users:detail", kwargs={"email": request.user.email})
        return Response({"redirect_url": request.build_absolute_uri(url)}) 

user_detail_api = UserDetailAPI.as_view()
user_update_api = UserUpdatedAPI.as_view()
user_redirect_api = UserRedirectAPI.as_view()