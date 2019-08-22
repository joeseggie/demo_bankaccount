from django.db.models import Sum
from django.utils.timezone import now
from rest_framework import permissions
from account.models import Transaction


class MaximumWithdrawPermission(permissions.BasePermission):

    message = 'Invalid withdraw amount'

    def has_permission(self, request, view):
        withdraw_amount = request.data['amount']
        transaction_total = Transaction.objects.filter(
            logged__year=now().today().year,
            logged__month=now().today().month,
            logged__day=now().today().day,
            transaction_type='withdraw',
            account_id=request.data['account_id']
        ).aggregate(Sum('amount'))
        if not transaction_total['amount__sum']:
            return False
        if not withdraw_amount:
            return False
        if withdraw_amount and int(withdraw_amount) <= 100000 \
                and int(transaction_total['amount__sum']) <= 100000:
            return True
        return False
