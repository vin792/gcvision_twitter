from __future__ import unicode_literals
from ..login_registration.models import User

from django.db import models

class FavoriteManager(models.Manager):
	def add_favorite(self, url, user_id):
		user = User.objects.get(id = user_id)
		new_favorite = Favorite.objects.create(url = url, user = user)
		return new_favorite

	def user_favorite_urls(self, user_id):
		user = User.objects.get(id = user_id)
		favorites = user.favorites.all()
		user_favorites = []
		for favorite in favorites:
			user_favorites.insert(0, favorite.url)
		return user_favorites

	def remove_favorite(self, favorite_id):
		Favorite.objects.filter(id = favorite_id).delete()


class Favorite(models.Model):
	user = models.ForeignKey(User, related_name = "favorites")
	url = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = FavoriteManager()