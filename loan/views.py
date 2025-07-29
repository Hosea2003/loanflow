from rest_framework import generics

from loan.models import Loan
from loan.permissions import IsConsultant, IsConsultantOrOwner
from loan.serializers import LoanCreateSerializer, LoanSerializer
from rest_framework.permissions import IsAuthenticated

from loan.tasks import assign_consultant_to_loan, send_loan_created_email
class LoanCreateView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        loan = serializer.save(user=self.request.user)
        send_loan_created_email.delay(loan.id)
        assign_consultant_to_loan.delay(loan.id)

class LoanListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsConsultant]

class LoanRetrieveView(generics.RetrieveAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsConsultantOrOwner]