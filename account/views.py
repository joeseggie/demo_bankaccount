from rest_framework import generics
from account.models import Account
from account.models import Transaction
from account.serializers import AccountSerializer
from account.serializers import TransactionSerializer
from account.permissions import MaximumWithdrawPermission


class AccountBalanceView(generics.RetrieveAPIView):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'account_number'


class AccountDepositView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class AccountWithdrawView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [MaximumWithdrawPermission]
