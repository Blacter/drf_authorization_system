from functools import wraps

from authorization_app.models import User, AccessAction
from rest_framework.request import Request
from rest_framework.response import Response

class AuthorizationService:
    def __init__(self, user_id: str):
        self._user_id = user_id

    @staticmethod
    def authorize(related_action: str) -> callable:
        def _authorize(view_method: callable) -> callable:
            @wraps(view_method)
            def view_with_authorization(self_for_inner_function, request: Request) -> Response:
                user_id: str = request.authentication_service.get_user_id()
                # Authorization
                authorization_service: AuthorizationService = AuthorizationService(user_id)
                if not authorization_service.is_access_to_action(related_action):
                    return Response({'error': 'access forbidden'}, status=403)
                return view_method(self_for_inner_function, request)
            return view_with_authorization
        return _authorize

    def is_access_to_action(self, action_name: str) -> bool:
        user = User.objects.get(id = self._user_id)
        action = AccessAction.objects.get(name=action_name)
        user_groups = user.groups.all()
        action_groups = action.groups.all()

        for user_group in user_groups:
            if user_group in action_groups:
                return True

        return False