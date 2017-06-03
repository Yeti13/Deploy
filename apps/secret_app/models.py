# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from random import randint


# Create your models here.
EMAILREG = re.compile(r'^[a-zA-Z0-9.+-_]+@[a-zA-Z0-9._-]+\.[a-zA-Z]*$')
PASSWORD_REGEX = re.compile(r'^(?=.*[^a-zA-Z])(?=.*[a-z])(?=.*[A-Z])\S{8,255}$')

class UserManager(models.Manager):

    def login(self, data):
        error = []
        # user = Users.objects.filter(email=data['logmail'], password=data['passlog'])
        # if not user:
        user = Users.objects.get(email=data['logmail'])
        if data['logmail'] != user.email or bcrypt.hashpw(data['passlog'].encode(), user.password.encode()) != user.password:
            error.append(["login", "Invalid email or password."])
        if error:
            print error
            return [False, error]
        else:
            return[True, user]

    def register(self, data):
        error = []
        if len(data['first_name']) < 1:
            error.append(["first_name", "First name is required."])
        if len(data['last_name']) < 1:
            error.append(["last_name", "Last name is required."])

        if len(data['email']) < 1:
            error.append(["email", "Email is required."])
        elif not EMAILREG.match(data['email']):
            error.append(["email", "Invalid email."])
        DB_check = Users.objects.filter(email=data['email'])
        if DB_check:
            error.append(["email", "Email already registered."])

        if len(data['password']) < 1:
            error.append(["password", "Password is required."])
        elif not PASSWORD_REGEX.match(data['password']):
            error.append(["password", "Invalid password."])

        if data['password'] != data['confirm']:
            error.append("confirm", "Password and password confirmation must match.")
        if error:
            return [False, error]

        else:
            hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            user = Users(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=hashed)
            user.save()

            return [True, user]

class SecretManager(models.Manager):

    def randAuthor(self):
        authors = ["Anonymous", "Who knows", "We'll never tell", "It's a secret"]
        random = authors[randint(0, 3)]
        return random

    def submit(self, data, user_id):
        error = []
        if len(data['secret']) < 1:
            error.append(["secret", "Secret cannot be blank"])
        if error:
            print error
            return [False, error]
        else:
            newSecret = Secrets.objects.create(secret=data['secret'], user=user_id)
            newSecret.save()
            return[True]

class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Secrets(models.Model):
    user = models.ForeignKey(Users)
    secret = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def hasLiked(self):
        return Users.objects.filter(user_like__secret=self)

    objects = SecretManager()

class Likes(models.Model):
    user = models.ForeignKey(Users, related_name="user_like")
    secret = models.ForeignKey(Secrets, related_name="sec_like")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
