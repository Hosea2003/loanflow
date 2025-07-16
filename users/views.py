from rest_framework import generics

from users.models import AppUser
from users.permissions import CanViewUser, IsConsultant
from users.serializers import CreateUserSerializer, DetailsUserSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    
class UserDetailsView(generics.RetrieveAPIView):
    lookup_field="id"
    queryset = AppUser.objects.all()
    permission_classes = [IsAuthenticated, CanViewUser]
    serializer_class = DetailsUserSerializer

class ListUserView(generics.ListAPIView):
    queryset = AppUser.objects.filter(role=AppUser.AppUserRoles.CLIENT)
    permission_classes = [IsAuthenticated, IsConsultant]
    serializer_class = DetailsUserSerializer