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

class LoanApproveDenyView(generics.UpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsConsultant]

    def update(self, request, *args, **kwargs):
        loan = self.get_object()
        action = request.data.get("action")

        if action not in ["accept", "deny"]:
            return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        if loan.status != LoanStatus.PENDING:
            return Response({"detail": "Loan already processed."}, status=status.HTTP_400_BAD_REQUEST)

        if action == "accept":
            loan.status = LoanStatus.ACCEPTED
        else:
            loan.status = LoanStatus.DENIED

        loan.save()
        return Response(self.get_serializer(loan).data)