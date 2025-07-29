from rest_framework import generics

from account.models import Beneficiary
from account.permissions import IsClient
from account.serializers import AccountSerializer, BeneficiarySerializer
from rest_framework.permissions import IsAuthenticated
from account.serializers import TransferSerializer
from rest_framework.response import Response
from rest_framework import status

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

class TransferView(generics.GenericAPIView):
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated, IsClient]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        return Response(
            TransferSerializer(transaction).data,
            status=status.HTTP_201_CREATED
        )
#