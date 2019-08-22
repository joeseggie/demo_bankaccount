"""Custom exceptions for the account app"""
from rest_framework import status
from rest_framework.exceptions import APIException


class ForbiddenWithdrawException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Invalid withdraw amount.'
