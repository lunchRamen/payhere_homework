from rest_framework import status
from rest_framework.exceptions import APIException


class UnauthorizedUser(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "인증되지 않은 사용자"
    code = "UNAUTHORIZED_USER"


class MoneyNull(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "돈은 필수 입력사항입니다."
    code = "MONEY_NULL"


class AlreadyTerminated(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "ALREADY_TERMINATED"
    default_code = "ALREADY_TERMINATED"