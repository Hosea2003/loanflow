from django.urls import path
from .views import LoanCreateView, LoanListView, LoanRetrieveView

urlpatterns = [
    path('loans/', LoanListView.as_view(), name='loan-list'),
    path('loans/create/', LoanCreateView.as_view(), name='loan-create'),
    path('loans/<int:pk>/', LoanRetrieveView.as_view(), name='loan-detail'),
]