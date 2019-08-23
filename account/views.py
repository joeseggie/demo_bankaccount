from uuid import UUID

from rest_framework import generics
from rest_framework.generics import get_object_or_404

from account.models import Account
from account.models import Transaction
from account.serializers import BalanceSerializer
from account.serializers import TransactionSerializer
from account.permissions import MaximumWithdrawPermission


class AccountBalanceView(generics.RetrieveAPIView):

    queryset = Account.objects.all()
    serializer_class = BalanceSerializer
    lookup_field = 'account_number'


class AccountDepositView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        account_id: UUID = UUID(self.request.data['account_id'])
        account = get_object_or_404(Account, pk=account_id)
        account.balance += int(self.request.data['amount'])
        serializer.save(account=account)


class AccountWithdrawView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [MaximumWithdrawPermission]

    def perform_create(self, serializer):
        account_id: UUID = UUID(self.request.data['account_id'])
        account = get_object_or_404(Account, pk=account_id)
        account.balance -= int(self.request.data['amount'])
        serializer.save(account=account)
