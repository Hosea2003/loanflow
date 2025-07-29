from django.urls import path

from account.views import AddBeneficiaryView, BeneficiaryView, TransferView

urlpatterns = [
    path("beneficiary/list", BeneficiaryView.as_view(), name='list-beneficiary'),
    path("beneficiary/add", AddBeneficiaryView.as_view(), name='add-beneficiary'),
    path("tranfer/", TransferView.as_view(), name='tranfer')
]