from django.urls import path
from .views import LoanApproveDenyView, LoanCreateView, LoanListView, LoanRetrieveView

urlpatterns = [
    path('', LoanListView.as_view(), name='loan-list'),
    path('create/', LoanCreateView.as_view(), name='loan-create'),
    path('<int:pk>/', LoanRetrieveView.as_view(), name='loan-detail'),
    path("<int:id>/approve-deny/", LoanApproveDenyView.as_view(), name='approve-deny')
]