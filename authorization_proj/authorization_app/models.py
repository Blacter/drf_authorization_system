import uuid

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class AccessAction(models.Model):
    name = models.CharField(unique=True, max_length=255)


class UserGroup(models.Model):
    name = models.CharField(unique=True, max_length=255)
    users = models.ManyToManyField('User', blank=True, related_name='groups')
    actions = models.ManyToManyField(
        'AccessAction', blank=True, related_name='groups')
