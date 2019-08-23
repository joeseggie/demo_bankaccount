from uuid import UUID

from rest_framework import generics
from rest_framework.generics import get_object_or_404

from account.models import Account
from account.models import Transaction
from account.serializers import BalanceSerializer
from account.serializers import TransactionSerializer
from account.permissions import MaximumWithdrawPermission
from account.permissions import InsufficientBalancePermission


class AccountBalanceView(generics.RetrieveAPIView):

    queryset = Account.objects.all()
    serializer_class = BalanceSerializer
    lookup_field = 'account_number'


class AccountDepositView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class AccountWithdrawView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [MaximumWithdrawPermission,
                          InsufficientBalancePermission]
