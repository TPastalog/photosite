from django.db import models
from datetime import datetime



class Albums(models.Model):
    class Meta():
        db_table = 'albums'
    title = models.CharField(max_length=250)
    text = models.TextField(default='')
    timestamp = models.DateTimeField(default=datetime.now)


class Images(models.Model):
    class Meta():
        db_table = 'images'
    title = models.CharField(max_length=250, verbose_name='Название вашей фотографии')
    text = models.TextField(default='', verbose_name='Расскажите что-нибудь о ней')
    image = models.ImageField(verbose_name='Выберите файл с фотографией')
    timestamp = models.DateTimeField(default=datetime.now)
    tag = models.CharField(max_length=20, default='', verbose_name='Придумайте интересный тэг')
    album = models.ForeignKey(Albums, to_field='id')