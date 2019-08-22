from rest_framework import serializers
from account.models import Account
from account.models import Transaction


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'account_number']


class TransactionSerializer(serializers.ModelSerializer):
    account_id = serializers.UUIDField(write_only=True)
    account = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['account_id', 'account', 'amount', 'transaction_type']
