from django.db import models
from django.utils.translation import gettext_lazy as _


class Artist(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('artist name'))
    desc = models.TextField(verbose_name=_('description'))
    photo = models.ImageField(blank=True, null=True, verbose_name='image',
                              upload_to='images/')

    def __str__(self):
        return self.name

    def get_plays(self):
        songs = Song.objects.filter(artists=self.id)
        sum_plays = 0
        for song in songs:
            sum_plays += song.plays
        return sum_plays

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
    is_public = models.BooleanField(default=False, verbose_name=_('is public'))
    file = models.FileField(verbose_name=_('file'), upload_to='albums/', blank=True, null=True)

    def __str__(self):
        artists_string = ''
        for artist in self.artists.all():
            artists_string += f'-{artist.name}'
        return f'{self.title}{artists_string}'

    def get_plays(self):
        songs = Song.objects.filter(album=self)
        sum_plays = 0
        for song in songs:
            sum_plays += song.plays
        return sum_plays

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')


class Song(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('song title'))
    desc = models.TextField(verbose_name=_('description'))
    cover = models.ImageField(blank=True, null=True, verbose_name='image',
                              upload_to='images/',
                              )
    artists = models.ManyToManyField(Artist, verbose_name=_('artists'), related_name='songs')
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name=_('album'))
    release_date = models.DateField(auto_now_add=True, verbose_name=_('release date'))
    file = models.FileField(verbose_name=_('file'), upload_to='musics/')
    lyrics = models.TextField(blank=True, null=True, verbose_name=_('lyrics'))
    plays = models.PositiveIntegerField(default=0, verbose_name=_('plays'))

    def __str__(self):
        artists_string = ''
        for artist in self.artists.all():
            artists_string += f'-{artist.name}'
        return f'{self.title}{artists_string}'

    class Meta:
        verbose_name = _('Song')
        verbose_name_plural = _('Songs')
