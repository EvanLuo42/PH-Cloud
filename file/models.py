from django.db import models
from django.utils.translation import gettext as _


class FileInfo(models.Model):
    file_id = models.BigAutoField(primary_key=True, verbose_name=_('File ID'))
    club_id = models.IntegerField(verbose_name=_('Club ID'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    file = models.FileField(verbose_name=_('File'))

    class Meta:
        verbose_name = _('File Info')
        verbose_name_plural = verbose_name
