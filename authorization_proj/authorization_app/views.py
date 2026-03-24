from pprint import pprint

from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.db import connection
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from authorization_app.models import User, UserGroup
from authorization_app.serializers import (
    SignupSerializer, LoginSerializer,
    UserProfileSerializer, UserEmailSerializer,
    UserGroupSerializer, )
from authorization_app.services.authentication_service import AuthenticationService
from authorization_app.services.authorization_service import AuthorizationService


class SignupAPI(APIView):
    serializer_class = SignupSerializer

    def post(self, request) -> Response:
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_new = serializer.save()
        return Response({'user_new': SignupSerializer(user_new).data})


class LoginAPI(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id: str = str(User.objects.get(
            email=serializer.validated_data['email']).id)

        request.authentication_service.do_login(user_id)
        login_result = {
            'login_result': 'success',
        }
        return Response({'login_result': login_result}, )


class LogoutAPI(APIView):
    def get(self, request: Request) -> Response:
        response = Response({'logout_result': 'success'})
        response.delete_cookie('jwt')
        return response


class DeleteProfileSoftAPI(APIView):
    def delete(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = User.objects.get(email=serializer.validated_data['email'])
        user.is_active = False
        user.save()

        response = Response({'delete_result': 'success'})
        response.delete_cookie('jwt')
        return response


class UserProfileAPI(APIView):
    @AuthenticationService.authenticate
    def patch(self, request: Request) -> Response:
        # request.authentication_service.authenticate_user()
        try:
            instance = User.objects.get(
                id=request.authentication_service.get_user_id())
        except:
            print(f'{request.authentication_service.get_user_id()=}')
            return Response({"error": "User does not exists"})

        user_profile_serializer = UserProfileSerializer(
            instance=instance,
            data=request.data,
            partial=True
        )
        user_profile_serializer.is_valid(raise_exception=True)
        update_result = user_profile_serializer.save()

        return Response({'update_result': UserProfileSerializer(update_result).data})


class Resource1API(APIView):
    @AuthenticationService.authenticate
    @AuthorizationService.authorize(related_action='s_action_1')
    def get(self, request: Request) -> Response:
        response = Response({'resource1': 'value1', 'resource1_2': 'value2'})
        return response


class Resource2API(APIView):
    @AuthenticationService.authenticate
    @AuthorizationService.authorize(related_action='vip_action_1')
    def get(self, request: Request) -> Response:
        return Response([{'resource2': 'value2', 'resource2_2': 'value2_2'}])


class Resource3API(APIView):
    @AuthenticationService.authenticate
    @AuthorizationService.authorize(related_action='admin_action_1')
    def get(self, request: Request) -> Response:
        return Response({'resource3': 'value3', 'resource3_2': 'value3_2'})


class AuthorizationControlGroupsAPI(APIView):
    # get_user_groups_with_actions
    @AuthenticationService.authenticate
    @AuthorizationService.authorize(related_action='admin_action_1')
    def get(self, request: Request) -> Response:
        pprint(connection.queries)
        result: list[dict] = []
        for user_group in UserGroup.objects.all():
            user_group_actions = user_group.actions.all()
            result.append({
                'user_group': user_group.name,
                'actions': [action.name for action in user_group_actions]
            })
        print('connection.queries =')
        print('-'*25)
        pprint(connection.queries)
        print('-'*25)
        return Response(result)


class AuthorizationControlUserAPI(APIView):
    @AuthenticationService.authenticate
    @AuthorizationService.authorize(related_action='admin_action_1')
    def get(self, request: Request) -> Response:
        user_email_serializer: UserEmailSerializer = UserEmailSerializer(
            data=request.query_params)
        user_email_serializer.is_valid(raise_exception=True)

        user = User.objects.get(
            email=user_email_serializer.validated_data['email'])
        user_groups = user.groups.all()

        result: dict = {
            'user_email': user.email,
            'related_user_groups': [user_group.name for user_group in user_groups]
        }

        return Response(result)


class AuthorizationControlAddUserInGroupAPI(APIView):
    @AuthenticationService.authenticate
    @AuthorizationService.authorize(related_action='admin_action_1')
    def post(self, request: Request) -> Response:
        user_email_serializer: UserEmailSerializer = UserEmailSerializer(
            data=request.data)
        user_email_serializer.is_valid(raise_exception=True)

        user_group_serializer: UserGroupSerializer = UserGroupSerializer(
            data=request.data
        )
        user_group_serializer.is_valid(raise_exception=True)

        user = User.objects.get(
            email=user_email_serializer.validated_data['email'])

        user.groups.add(UserGroup.objects.get(
            name=user_group_serializer.validated_data['group_name']
        ))

        result = {
            'email': user_email_serializer.validated_data['email'],
            'group_name': user_group_serializer.validated_data['group_name'],
            'operation_result': 'success',
        }

        return Response(result)


class AuthorizationControlDeleteUserInGroupAPI(APIView):
    @AuthenticationService.authenticate
    @AuthorizationService.authorize(related_action='admin_action_1')
    def post(self, request: Request) -> Response:
        user_email_serializer: UserEmailSerializer = UserEmailSerializer(
            data=request.data)
        user_email_serializer.is_valid(raise_exception=True)

        user_group_serializer: UserGroupSerializer = UserGroupSerializer(
            data=request.data
        )
        user_group_serializer.is_valid(raise_exception=True)

        user = User.objects.get(
            email=user_email_serializer.validated_data['email'])

        user.groups.remove(UserGroup.objects.get(
            name=user_group_serializer.validated_data['group_name']
        ))

        result = {
            'email': user_email_serializer.validated_data['email'],
            'group_name': user_group_serializer.validated_data['group_name'],
            'operation_result': 'success',
        }

        return Response(result)

