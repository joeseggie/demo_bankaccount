from rest_framework.test import APITestCase
from account.models import Account
from rest_framework.reverse import reverse
from rest_framework import status


class AccountTestCase(APITestCase):

    def setUp(self):
        self.account_obj = Account.objects.create(
            first_name='Joseph',
            last_name='Serunjogi',
            account_number='0001112223231'
        )

    def test_account_balance(self):
        response = self.client.get(reverse('account-balance',
                                           kwargs={'account_number': self.account_obj.account_number}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_deposit(self):
        response = self.client.post(
            reverse('account-deposit'),
            {
                'account_id': self.account_obj.id,
                'transaction_type': 'deposit',
                'amount': 4000
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_account_withdraw(self):
        response = self.client.post(
            reverse('account-withdraw'),
            {
                'account_id': self.account_obj.id,
                'transaction_type': 'withdraw',
                'amount': 1000
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_account_withdraw_beyond_maximum(self):
        response = self.client.post(
            reverse('account-withdraw'),
            {
                'account_id': self.account_obj.id,
                'transaction_type': 'withdraw',
                'amount': 120000
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
