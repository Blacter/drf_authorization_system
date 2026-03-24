from django.http import HttpRequest, HttpResponse

from authorization_app.services.authentication_service import AuthenticationService

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        jwt: str | None = request.COOKIES.get('jwt')
        if jwt is not None:
            jwt = jwt.strip()
        authentication_service: AuthenticationService = AuthenticationService(jwt)
        setattr(request, 'authentication_service', authentication_service)

        response = self.get_response(request)

        if request.authentication_service.is_login():
            print('Trace 1')
            jwt = request.authentication_service.get_token()
            response.set_cookie(
                key='jwt',
                value=jwt,
                httponly=True,
            )
        return response