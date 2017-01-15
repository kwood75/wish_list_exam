from __future__ import unicode_literals
from django.db import models
import bcrypt
from datetime import datetime
import re

name_regex = re.compile("^[a-zA-Z\s]+$")

class UserManager(models.Manager):
    def register(self, input):
        errors = []

        if len(input['name']) < 3:
            errors.append('Name can not be less than 3 characters')

        if not name_regex.match(input['name']):
            errors.append('Name can contain letters only')

        if len(input['username']) < 3:
            errors.append('Username can not be less than 3 characters')

        if input['password'] != input['confirm']:
            errors.append('Passwords do not match. Try again')

        if len(input['password']) < 8:
            errors.append('Password must be at least 8 characters')

        same = Person.objects.filter(username=input['username'])
        if same:
            errors.append('Username is already in use')

        if not input['hire_date']:
            errors.append('Please enter the date hired')
        else:
            date = datetime.strptime(input['hire_date'], "%Y-%m-%d")
            if datetime.today() <= date:
                errors.append('Hire date cannot be after today')

        if len(errors) == 0:
            pwHash = bcrypt.hashpw(input['password'].encode(), bcrypt.gensalt().encode())
            user = Person.objects.create(name=input['name'], username=input['username'], hire_date=input['hire_date'], password=pwHash)
            return (True, user)

        else:
            return (False, errors)

    def login(self, input):
        errors = []
        user = Person.objects.filter(username=input['username'])
        if user.exists():
            InputPw = input['password'].encode()
            HashPw = user[0].password.encode()

            if bcrypt.checkpw(InputPw, HashPw):
                return (True, user[0])
            else:
                errors.append(("Username and password does not exist!"))
        else:
            errors.append(("Username and password does not exist!"))
        return (False, errors)

class Person(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    hire_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
