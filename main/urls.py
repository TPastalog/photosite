from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.log_in, name = 'login'),
    url(r'^logout/$', views.log_out, name = 'logout'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^add_album/$', views.add_album, name = 'add_album'),
    url(r'^add_image/$', views.add_image, name = 'add_image'),
    url(r'^add_image/(?P<album_id>\d+)/$', views.add_image, name = 'add_image'),
    url(r'^edit_album/(?P<album_id>\d+)/$', views.edit_album, name = 'edit_album'),
    url(r'^delete/(?P<album_id>\d+)/$', views.delete_album, name = 'delete_album'),
    url(r'^(?P<album_id>\d+)/(?P<photo_id>\d+)/$', views.photo, name = 'photo'),
    url(r'^edit_image/(?P<album_id>\d+)/(?P<photo_id>\d+)/$', views.edit_image, name = 'edit_image'),
    url(r'^delete/(?P<album_id>\d+)/(?P<photo_id>\d+)/$', views.delete_image, name = 'delete_image'),
    url(r'^(?P<album_id>\d+)/page/(?P<page_number>\d+)/$', views.album, name='album'),
    url(r'^(?P<album_id>\d+)/$', views.album, name='album'),
    url(r'^Tags/(?P<tag>[^/]+)/$', views.Tags, name='Tags'),
    url(r'^Tags/(?P<tag>[^/]+)/page/(?P<page_number>\d+)/$', views.Tags, name='Tags'),
    url(r'^Tag/(?P<photo_id>\d+)/$', views.Tag, name='Tag'),
    url(r'^page/(?P<page_number>\d+)/$', views.index, name='index'),
    url(r'^$', views.index, name = 'index'),

]