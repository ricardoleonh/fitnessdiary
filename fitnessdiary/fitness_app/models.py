from django.db import models
import re
import bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager): # Validates the regitration form is complete and the email and phone are not in use
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) == 0:
            errors['first_name'] = "First Name is Required"
        if len(postData['first_name']) < 2 or postData['first_name'].isalpha() != True:
            errors['first_name'] = "First Name must be at least 2 characters long"
        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last Name is Required"
        if len(postData['last_name']) < 2 or postData['last_name'].isalpha() != True:
            errors['last_name'] = "Last Name must be at least 2 characters long"
        if len(postData['user_name']) == 0:
            errors['user_name'] = "User Name is Required"
        if len(postData['user_name']) < 5:
            errors['user_name'] = "User Name must be at least 5 characters long"
        existing_user_name = User.objects.filter(user_name=postData['user_name'])
        if len(existing_user_name) > 0:
            errors['user_name'] = "User Name already in use"
        if len(postData['email']) == 0:
            errors['email'] = "Email is Required"
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) > 0:
            errors['email'] = "Email already in use"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Invalid Email Format"
        if len(postData['password']) == 0:
            errors['password'] = "Password is Required"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 Characters"
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password and Confirm Password must match!"
        return errors

    def log_validator(self, postData):
        errors = {}
        if len(postData['user_name']) == 0:
            errors['user_name'] = "User Name is required"
        existing_user_name = User.objects.filter(user_name=postData['user_name'])
        if len(existing_user_name) != 1:
            errors['user_name'] = "User not Found!"
        elif len(postData['password']) == 0:
            errors['password'] = "Password Required"
        elif not bcrypt.checkpw(postData['password'].encode(), existing_user_name[0].password.encode()):
            errors['user_name'] = "User Name and password do no match"
        return errors


class User(models.Model):
    user_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=40)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Routine(models.Model):
    routine_name = models.CharField(max_length=45)
    chest_a = models.CharField(max_length=45)
    chest_b = models.CharField(max_length=45)
    chest_c = models.CharField(max_length=45)
    back_a = models.CharField(max_length=45)
    back_b = models.CharField(max_length=45)
    back_c = models.CharField(max_length=45)
    legs_a = models.CharField(max_length=45)
    legs_b = models.CharField(max_length=45)
    legs_c = models.CharField(max_length=45)
    arms_a = models.CharField(max_length=45)
    arms_b = models.CharField(max_length=45)
    arms_c = models.CharField(max_length=45)
    routine_creator = models.ForeignKey(User, related_name='routines_crated', on_delete=models.CASCADE)
    routines_added_by = models.ManyToManyField(User, related_name='routine_added')
    completed_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

     
