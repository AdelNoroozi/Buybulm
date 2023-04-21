from django.db import models
from django.utils.translation import gettext_lazy as _


class Artist(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('artist name'))
    desc = models.TextField(verbose_name=_('description'))
    photo = models.ImageField(blank=True, null=True, verbose_name='image',
                              upload_to='images/')

    class Meta:
        verbose_name = _('Artist')
        verbose_name_plural = _('Artists')


class Album(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('album title'))
    desc = models.TextField(verbose_name=_('description'))
    release_date = models.DateField(auto_now_add=True, verbose_name=_('release date'))
    artists = models.ManyToManyField(Artist, verbose_name=_('artists'))
    cover = models.ImageField(blank=True, null=True, verbose_name='image',
                              upload_to='images/')
    min_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('minimum price'))

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')


class Song(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('song title'))
    desc = models.TextField(verbose_name=_('description'))
    cover = models.ImageField(blank=True, null=True, verbose_name='image',
                              upload_to='images/',
                              )
    artists = models.ManyToManyField(Artist, verbose_name=_('artists'))
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE, verbose_name='album')
    release_date = models.DateField(auto_now_add=True, verbose_name=_('release date'))
    file = models.FileField(verbose_name=_('file'), upload_to='musics/')
    lyrics = models.TextField(blank=True, null=True, verbose_name=_('lyrics'))
    plays = models.PositiveIntegerField(default=0, verbose_name=_('plays'))

    class Meta:
        verbose_name = _('Song')
        verbose_name_plural = _('Songs')
