from django.urls import path

from account.views import AccountBalanceView
from account.views import AccountDepositView
from account.views import AccountWithdrawView

urlpatterns = [
    path('deposit/', AccountDepositView.as_view(), name='account-deposit'),
    path('withdraw/', AccountWithdrawView.as_view(), name='account-withdraw'),
    path('<str:account_number>/', AccountBalanceView.as_view(), name='account-balance'),
]
