import qrcode
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def _create_user(self, username, password, email, **kwargs):
        if not username:
            raise ValueError('The given username must be set')
        if not password:
            raise ValueError('The given password must be set')
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = False
        return self._create_user(username, password, email, **kwargs)

    def create_superuser(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        user = self._create_user(username, password, email, **kwargs)
        device = TOTPDevice.objects.create(user=user, name=username, confirmed=True)
        device.save()
        qr = qrcode.QRCode()
        qr.add_data(device.config_url)
        qr.print_ascii()
        print('\n' + device.config_url + '\n')
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True, verbose_name=_('User ID'))
    username = models.CharField(max_length=30, unique=True, verbose_name=_('Username'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is a stuff'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('Is a superuser'))
    email = models.EmailField(unique=True, verbose_name=_('Email'))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['is_staff', 'is_superuser', 'email']

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = verbose_name


class Club(models.Model):
    club_id = models.BigAutoField(primary_key=True, verbose_name=_('Club ID'))
    club_name = models.CharField(max_length=30, unique=True, verbose_name=_('Club Name'))
    owner_email = models.EmailField(unique=True, verbose_name=_('Email'))

    class Meta:
        verbose_name = _('Club')
        verbose_name_plural = verbose_name
