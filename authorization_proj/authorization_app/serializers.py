from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator

from rest_framework import serializers

from authorization_app.models import User, UserGroup

name_acceptable_characters = RegexValidator(
    r'^[a-zA-Zа-яА-ЯёЁ]*$', message='Wrong characters')


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(
        allow_null=True,
    )
    first_name = serializers.CharField(
        min_length=2, max_length=255, trim_whitespace=True,
        validators=[name_acceptable_characters]
    )
    surname = serializers.CharField(
        min_length=2, max_length=255, trim_whitespace=True,
        validators=[name_acceptable_characters]
    )
    patronymic = serializers.CharField(
        min_length=2, max_length=255, trim_whitespace=True,
        validators=[name_acceptable_characters]
    )
    email = serializers.EmailField(
        min_length=2, max_length=255, trim_whitespace=True
    )
    password = serializers.CharField(
        min_length=8, max_length=255, trim_whitespace=True, write_only=True
    )
    is_active = serializers.BooleanField()


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        min_length=2, max_length=255, trim_whitespace=True,
        validators=[name_acceptable_characters]
    )
    surname = serializers.CharField(
        min_length=2, max_length=255, trim_whitespace=True,
        validators=[name_acceptable_characters]
    )
    patronymic = serializers.CharField(
        min_length=2, max_length=255, trim_whitespace=True,
        validators=[name_acceptable_characters]
    )
    email = serializers.EmailField(
        min_length=2, max_length=255, trim_whitespace=True
    )
    password = serializers.CharField(
        min_length=8, max_length=255, trim_whitespace=True, write_only=True
    )
    password_repeat = serializers.CharField(
        min_length=8, max_length=255, trim_whitespace=True, write_only=True
    )

    def validate(self, data):
        try:
            User.objects.get(email=data['email'])
        except User.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError('email already exists')

        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError('passwords did not match')
        return data

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            first_name=validated_data['first_name'],
            surname=validated_data['surname'],
            patronymic=validated_data['patronymic'],
        )

        user.groups.add(UserGroup.objects.get(name='simple_user'))

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        min_length=2, max_length=255, trim_whitespace=True
    )
    password = serializers.CharField(
        min_length=8, max_length=255, trim_whitespace=True,
        write_only=True
    )

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        if user.is_active == False:
            raise serializers.ValidationError('User deleted')

        user_password = data['password']
        user_password_hash = user.password
        if not check_password(user_password, user_password_hash):
            raise serializers.ValidationError('Wrong password')
        return data


class UserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        min_length=2, max_length=255, trim_whitespace=True,
        validators=[name_acceptable_characters],
    )
    surname = serializers.CharField(
        min_length=2, max_length=255, trim_whitespace=True,
        validators=[name_acceptable_characters],
    )
    patronymic = serializers.CharField(
        min_length=2, max_length=255, trim_whitespace=True,
        validators=[name_acceptable_characters],
    )
    email = serializers.EmailField(
        min_length=2, max_length=255, trim_whitespace=True,
        read_only=True
    )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.patronymic = validated_data.get(
            'patronymic', instance.patronymic)
        instance.save()
        return instance

class JWTSerializer(serializers.Serializer):
    jwt = serializers.CharField(trim_whitespace=True,)


class UserGroupSerializer(serializers.Serializer):
    group_name = serializers.CharField(trim_whitespace=True)

    def validate(self, data):
        try:
            group = UserGroup.objects.get(name=data['group_name'])
        except UserGroup.DoesNotExist:
            raise serializers.ValidationError('UserGroup does not exist')
        return data


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        min_length=2, max_length=255, trim_whitespace=True
    )

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        return data
