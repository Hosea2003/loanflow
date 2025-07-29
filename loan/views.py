from rest_framework import generics

from loan.models import Loan
from loan.permissions import IsConsultant, IsConsultantOrOwner
from loan.serializers import LoanCreateSerializer, LoanSerializer
from rest_framework.permissions import IsAuthenticated
class LoanCreateView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LoanListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsConsultant]

class LoanRetrieveView(generics.RetrieveAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsConsultantOrOwner]