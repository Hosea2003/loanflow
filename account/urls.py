from django.urls import path

from account.views import AddBeneficiaryView, BeneficiaryView

urlpatterns = [
    path("beneficiary/list", BeneficiaryView.as_view(), name='list-beneficiary'),
    path("beneficiary/add", AddBeneficiaryView.as_view(), name='add-beneficiary')
]