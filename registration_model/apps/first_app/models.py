from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import datetime, date
Email_Regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def registration(self, request):

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email'].lower()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        bday = request.POST['bday']

        errors = []

        valid = True
        if len(email) < 1 or len(first_name) < 1 or len(last_name) < 1 or len(password) < 1 or len(confirm_password)< 1 or len(bday) <1:
            errors.append("A field can not be empty")
            valid = False
        else:
            # names
            if len(first_name) < 2 or len(last_name) < 2:
                errors.append("Name field needs at least two characters")
                valid = False
            elif first_name.isalpha() == False or last_name.isalpha() == False:
                errors.append("Name field needs to be all letters")
                valid = False
            # email
            if not Email_Regex.match(email):
                errors.append("Field required in email format")
                valid = False
            # password
            if len(password) < 8:
                errors.append("Password needs at least 8 characters")
                valid = False
            elif password != confirm_password:
                errors.append("Password and confirm password needs to match")
                valid = False
            if bday == unicode(datetime.today().date()) or bday > unicode(datetime.today().date()):
                errors.append('Birthday needs to be in past')
                valid = False

        if valid:
            distinct_list = User.objects.filter(email = email)
            if not distinct_list:
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
                return (True, user)
            else:
                # valid_messages.append("Email already exists")
                errors.append("Email already exists")

        return (False, errors)


    def login(self, request):
        if request.method == "POST":
            email = request.POST['email_log'].lower()
            password = request.POST['password_log']

            login_messages = []

            if len(email) < 1 or len(password) < 1:
                login_messages.append("A field can not be empty")

            if not Email_Regex.match(email):
                login_messages.append("Field required in email format")

            if len(password) < 8:
                login_messages.append("Password needs at least 8 characters")

            if not login_messages:
                user = User.objects.filter(email=email)
                if user:
                    if bcrypt.hashpw(password.encode(), user[0].password.encode()) == user[0].password.encode():
                        return True, user[0]
                    else:
                        login_messages.append("Wrong password")
                else:
                    login_messages.append("Not a registered user")

        return False, login_messages


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
