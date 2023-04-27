from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile
from music_bot.models import Album


class Payment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='payments', verbose_name=_('user'))
    album = models.ForeignKey(Album, on_delete=models.PROTECT, related_name='payments', verbose_name=_('album'))
    payment_time = models.DateTimeField(auto_now_add=True, verbose_name=_('payment time'))
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('price'))
    receipt = models.FileField(verbose_name=_('receipt'), upload_to='payments/')
    message = models.TextField(verbose_name=_('message'))
    user_preview_name = models.CharField(max_length=20, verbose_name=_('user preview name'))

    def __str__(self):
        return f'{self.user.parent_base_user.email}-{self.album.title}'

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        unique_together = (('user', 'album'),)
        index_together = (('user', 'album'),)
