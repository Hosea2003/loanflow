from rest_framework import generics

from account.models import Beneficiary
from account.serializers import BeneficiarySerializer
from rest_framework.permissions import IsAuthenticated

class BeneficiaryView(generics.ListAPIView):
    serializer_class = BeneficiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Beneficiary.objects.filter(
            user=user
        )

class AddBeneficiaryView(generics.CreateAPIView):
    serializer_class = BeneficiarySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
