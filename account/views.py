from rest_framework import generics

from account.models import Beneficiary
from account.permissions import IsClient
from account.serializers import AccountSerializer, BeneficiarySerializer
from rest_framework.permissions import IsAuthenticated

class BeneficiaryView(generics.ListAPIView):
    serializer_class = BeneficiarySerializer
    permission_classes = [IsAuthenticated, IsClient]

    def get_queryset(self):
        user = self.request.user
        return Beneficiary.objects.filter(
            user=user
        )

class AddBeneficiaryView(generics.CreateAPIView):
    serializer_class = BeneficiarySerializer
    permission_classes = [IsAuthenticated, IsClient]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class ListAccountView(generics.ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsClient]