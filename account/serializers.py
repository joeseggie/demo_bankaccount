from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from account.models import Account
from account.models import Transaction


class BalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['account_number', 'first_name', 'last_name', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    account_id = serializers.UUIDField(write_only=True)
    account = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['account_id', 'account', 'amount', 'transaction_type']

    def create(self, validated_data):
        account_update: Account = get_object_or_404(
            Account,
            pk=validated_data.get('account_id'))
        if validated_data.get('transaction_type') == 'deposit':
            account_update.balance += int(validated_data.get('amount'))
        if validated_data.get('transaction_type') == 'withdraw':
            account_update.balance -= int(validated_data.get('amount'))
        account_update.save()

        return Transaction.objects.create(**validated_data)

