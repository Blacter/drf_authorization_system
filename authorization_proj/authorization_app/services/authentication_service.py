from functools import wraps

from rest_framework.exceptions import AuthenticationFailed

from django.conf import settings
from authorization_app.services.jwt_service import JWTService

from rest_framework.request import Request
from rest_framework.response import Response

class AuthenticationService:
    def __init__(self, jwt: str | None):
        self._is_login: bool = False
        self._jwt_service: JWTService = JWTService(jwt, settings.JWT_EXP)

    @staticmethod
    def authenticate(view_method: callable) -> callable:
        @wraps(view_method)
        def view_with_authentication(self_for_inner_function, request: Request) -> Response:
            try:
                request.authentication_service.authenticate_user()
            except AuthenticationFailed as e:
                return Response({'error': str(e)}, status=401)
            return view_method(self_for_inner_function, request)

        return view_with_authentication

    def authenticate_user(self) -> None:
        self._jwt_service.decode_jwt_if_valid()
        if not self._jwt_service.is_token_valid():
            raise AuthenticationFailed('authentication failed', code=401)

    def get_token(self) -> tuple[bytes, bytes]:
        jwt: bytes = self._jwt_service.get_jwt_token()
        return jwt

    def get_new_tokens(self, user_id) -> tuple[bytes, bytes]:
        jwt: bytes = self._jwt_service.get_new_jwt_token(user_id)
        return jwt

    def do_login(self, user_id) -> None:
        self._is_login: bool = True
        self._jwt_service.get_new_jwt_token(user_id)

    def get_new_jwt(self, user_id: str, jwt_age: int) -> None:
        self._is_jwt_refresh: bool = True

    def get_user_id(self) -> str:
        return self._jwt_service.user_id

    def is_login(self) -> bool:
        return self._is_login

