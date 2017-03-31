from __future__ import unicode_literals
import bcrypt
import re

from django.db import models

class UserManager(models.Manager):
	def login(self, email, password):
		user_confirm = User.objects.filter(email=email)
		if user_confirm:
			for user in user_confirm:
				user_password = user.hash_password
				user_id = user.id
			password = password.encode('utf-8')
			user_password = user_password.encode('utf-8')
			if bcrypt.hashpw(password, user_password) == user_password:
				return (True, user_id)
			else:
				return (False, "Invalid password")
		else:
			return (False, "No user with that email")

	def register(self, first_name, last_name, email, password, password_confirm):
		errors = []
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
		email_exists = User.objects.filter(email=email)
		if len(first_name) < 2:
			errors.append("First name must be more than 2 characters")
		if not NAME_REGEX.match(first_name):
			errors.append("First name can only contain letters")
		if len(last_name) < 2:
			errors.append("Last name must be more than 2 characters")
		if not NAME_REGEX.match(last_name):
			errors.append("Last name can only contain letters")
		if not EMAIL_REGEX.match(email):
			errors.append("Not a valid email")
		if email_exists:
			errors.append("Email already in use")
		if len(password) < 8:
			errors.append("Password must be more than 8 characters")
		if password != password_confirm:
			errors.append("Passwords must match")
		password = password.encode('utf-8')
		hashed = bcrypt.hashpw(password, bcrypt.gensalt())
		if errors:
			return errors
		else:
			self.create(first_name=first_name, last_name=last_name, email=email, hash_password=hashed)
			new_user = User.objects.get(email = email)
			return (True, new_user.id)

class User(models.Model):
	first_name = models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)
	email = models.EmailField()
	hash_password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

