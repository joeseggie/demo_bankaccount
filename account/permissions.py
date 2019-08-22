from django.db.models import Sum
from django.utils.datetime_safe import datetime
from rest_framework import permissions

from account.exceptions import ForbiddenWithdrawException
from account.models import Transaction
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
