from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^imageupload$', views.upload_image, name = 'upload_image'),
    url(r'^favorites$', views.favorites, name = 'favorites'),
    url(r'^addfavorite$', views.add_favorite, name = 'add_favorite'),
    url(r'^removefavorite/(?P<favorite_id>\d+)$', views.remove_favorite, name = 'remove_favorite')
]
