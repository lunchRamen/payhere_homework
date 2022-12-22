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


class MoneyZero(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "가계부의 생성,수정은 0원이 넘어야 가능합니다."
    default_code = "NOT_ALLOW_MONEY_0"


class NoAccountBook(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "없는 가계부 조회는 불가합니다."
    default_code = "NO_ACCOUNTBOOK"