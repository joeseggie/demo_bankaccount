from uuid import UUID

from django.db.models import Sum
from django.utils.datetime_safe import datetime
from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from account.exceptions import ForbiddenWithdrawException
from account.exceptions import InsufficientBalanceException
from account.models import Transaction, Account
from common.constants import WITHDRAW_THRESHOLD


class MaximumWithdrawPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        withdraw_amount_input = request.data['amount']
        if withdraw_amount_input:
            withdraw_amount: int = int(withdraw_amount_input)

            withdraw_sum_dict: dict = Transaction.objects\
                .filter(
                    logged__year=datetime.today().year,
                    logged__month=datetime.today().month,
                    logged__day=datetime.today().day,
                    transaction_type='withdraw',
                    account_id=request.data['account_id']
                )\
                .aggregate(Sum('amount'))

            current_withdraw: int = int(withdraw_sum_dict['amount__sum']) \
                if withdraw_sum_dict['amount__sum'] else 0
            if (current_withdraw + withdraw_amount) <= WITHDRAW_THRESHOLD:
                return True

        raise ForbiddenWithdrawException


class InsufficientBalancePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        withdraw_amount: int = int(request.data['amount'])
        account_id: UUID = UUID(request.data['account_id'])
        account: Account = get_object_or_404(Account, pk=account_id)
        if withdraw_amount > account.balance:
            raise InsufficientBalanceException
        return True
