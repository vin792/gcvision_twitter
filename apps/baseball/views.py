from django.shortcuts import render, redirect, reverse
from . services import *
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Favorite, User
import base64

def index(request):
	if 'user_id' in request.session:
		if 'img_description' not in request.session:
			return render(request, 'baseball/index.html')
		else:
			context = {
				'tweets': twitterSearch(request.session['img_description']),
				'user_favorites': Favorite.objects.user_favorite_urls(request.session['user_id'])
			}
			return render(request, 'baseball/index.html', context)
	else:
		return redirect(reverse("login:index"))

def upload_image(request):
	if request.method == 'POST' and request.FILES['logo_image']:
		myfile = request.FILES['logo_image'].read()
		encoded_string = base64.b64encode(myfile)
		request.session['img_description'] = visionCall(encoded_string)
        return redirect(reverse('baseball:index'))

def favorites(request):
	user = User.objects.get(id = request.session['user_id'])
	context = {
		'tweets': user.favorites.all().order_by('-created_at')
	}
	return render(request, 'baseball/favorites.html', context)

def add_favorite(request):
	if request.method == "POST":
		url = request.POST['url']
		model_response = Favorite.objects.add_favorite(url, request.session['user_id'])
		return render(request, 'baseball/posts_addfavorite.html')

def remove_favorite(request, favorite_id):
	if request.method == 'POST':
		Favorite.objects.remove_favorite(favorite_id)
		return redirect(reverse('baseball:favorites'))