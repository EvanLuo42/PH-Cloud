from django.core.cache import cache
from django.forms import fields, Form

from django.utils.translation import gettext as _

from user.models import User, Club


class LoginForm(Form):
    email = fields.RegexField(
        required=True,
        regex='[a-zA-Z0-9_]+@shphschool.com',
        max_length=40,
        error_messages={
            'required': _('Email can not be empty.'),
            'max_length': _('Email is too long.'),
            'invalid': _('Email is illegal or not a Pinghe email')
        }
    )

    password = fields.CharField(
        required=True,
        error_messages={
            'required': _('Password can not be empty.')
        }
    )


class RegisterForm(Form):
    username = fields.CharField(
        required=True,
        min_length=4,
        max_length=30,
        error_messages={
            'required': _('Username can not be empty.'),
            'min_length': _('Username is too short.'),
            'max_length': _('Username is too long.')
        }
    )

    password = fields.CharField(
        required=True,
        error_messages={
            'required': _('Password can not be empty.')
        }
    )

    email = fields.RegexField(
        required=True,
        regex='[a-zA-Z0-9_]+@shphschool.com',
        max_length=40,
        error_messages={
            'required': _('Username can not be empty.'),
            'max_length': _('Email is too long.'),
            'invalid': _('Email is illegal or not a Pinghe email')
        }
    )

    captcha = fields.CharField(
        required=True,
        error_messages={
            'required': _('Captcha can not be empty.')
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise fields.ValidationError(_('User is already exist.'))
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise fields.ValidationError(_('Email is already exist.'))
        if not Club.objects.filter(owner_email=email).exists():
            raise fields.ValidationError(_('Email was not signed up.'))

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.data.get('email')
        if User.objects.filter(email=email).exists():
            raise fields.ValidationError(_('User is already exist.'))
        else:
            if cache.get(email) == captcha:
                return captcha
            else:
                raise fields.ValidationError(_('Captcha is not correct.'))


class EmailForm(Form):
    email = fields.RegexField(
        required=True,
        regex='[a-zA-Z0-9_]+@shphschool.com',
        max_length=40,
        error_messages={
            'required': _('Email can not be empty.'),
            'max_length': _('Email is too long.'),
            'invalid': _('Email is illegal or not a Pinghe email')
        }
    )
