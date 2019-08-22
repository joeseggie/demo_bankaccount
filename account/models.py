from uuid import uuid4

from django.db import models
from django.utils.timezone import now


class Account(models.Model):
    """Model to hold account information"""
    id = models.UUIDField(primary_key=True, default=uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.account_number


class Transaction(models.Model):
    """Model to hold account transactions"""
    account = models.ForeignKey(Account,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
    logged = models.DateTimeField(default=now, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20,
        choices=[('withdraw', 'withdraw'),
                 ('deposit', 'deposit')])
