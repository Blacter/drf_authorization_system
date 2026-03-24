import datetime

import jwt
from django.conf import settings

from authorization_app.services.expire_datetime_service import ExpireDatetimeService
from authorization_app.models import User

type Header = dict[str, str]
type Payload = dict[str, str]

class JWTNotInCookiesErrors(Exception):
    def __str__(self) -> str:
        return 'jwt not in cookies'

class JWTService:
    _expire_datetime_service: ExpireDatetimeService = ExpireDatetimeService()

    def __init__(self, jwt_token: str | None, token_age: int):
        self._is_token_chenged: bool = False
        self._decoded: dict | None = None
        self._jwt_token: str | None = jwt_token
        self._token_age: int = token_age

        self._is_token_valid: bool | None = None

    def decode_jwt_if_valid(self) -> bool:
        self._decode_jwt_if_valid()

    def _decode_jwt_if_valid(self) -> None:
        if self._jwt_token is None:
            self._is_token_valid = False
        try:
            self._decoded = jwt.decode(
                self._jwt_token,
                settings.UNSAVE_SECRET_KEY,
                algorithms=["HS256"]
            )
            User.objects.get(id=self._decoded.get('userId'))

        except jwt.InvalidSignatureError:
            self._is_token_valid = False
        except jwt.ExpiredSignatureError:
            self._is_token_valid = False
        except jwt.InvalidTokenError:
            self._is_token_valid = False
        except User.DoesNotExist:
            self._decoded = None
            self._is_token_valid = False
        else:
            self._is_token_valid = True

    def is_token_valid(self) -> bool:
        if self._jwt_token is None:
            return False
        if self._is_token_valid is None:
            self._decode_jwt()
        return self._is_token_valid

    @property
    def user_id(self) -> str:
        if self._decoded is None:
            return None
        return self._decoded.get('userId')

    def get_jwt_token(self) -> bytes:
        return self._jwt_token

    def get_new_jwt_token(self, user_id: str) -> bytes:
        self._is_token_chenged = True
        self._generate_new_jwt_token(user_id)
        return self._jwt_token

    def _generate_new_jwt_token(self, user_id: str) -> bytes:
        header: Header = {
            'alg': 'HS256',
            'typ': 'JWT'
        }
        payload: Payload = {
            'userId': user_id,
            # TODO разобраться как задавать exp и как проверять exp.
            'exp': self._expire_datetime_service.get_new_expire_date(self._token_age),
        }
        token = jwt.encode(
            payload,
            key = settings.UNSAVE_SECRET_KEY,
            algorithm='HS256',
            headers=header
        )
        self._jwt_token = token

    def is_token_changed(self) -> bool:
        return self._is_token_chenged
