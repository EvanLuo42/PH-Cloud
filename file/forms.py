from django.forms import Form, fields

from django.utils.translation import gettext as _

from file.models import FileInfo
from user.models import Club


class FileUploadForm(Form):
    club_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('Club ID can not be empty.')
        }
    )

    file_name = fields.CharField(
        required=True,
        min_length=4,
        max_length=40,
        error_messages={
            'required': _('File name can not be empty.'),
            'min_length': _('File name is too short.'),
            'max_length': _('File name is too long.')
        }
    )

    file = fields.FileField(
        required=True,
        max_length=100,
        error_messages={
            'required': _('File can not be empty.')
        }
    )

    def clean_club_id(self):
        club_id = self.cleaned_data.get('club_id')
        if not Club.objects.filter(club_id=club_id).exists():
            raise fields.ValidationError(_('Club is not existed'))
        else:
            return club_id


class GetFileForm(Form):
    file_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('File ID can not be empty.')
        }
    )

    def clean_file_id(self):
        file_id = self.cleaned_data.get('file_id')
        if not FileInfo.objects.filter(file_id=file_id).exists():
            raise fields.ValidationError(_('File is not existed'))
        else:
            return file_id


class GetAllFilesUnderClubForm(Form):
    club_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('Club ID can not be empty.')
        }
    )

    def clean_club_id(self):
        club_id = self.cleaned_data.get('club_id')
        if not Club.objects.filter(club_id=club_id).exists():
            raise fields.ValidationError(_('Club is not existed'))
        else:
            return club_id

