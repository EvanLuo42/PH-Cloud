"""ph_cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from django_otp.admin import OTPAdminSite

import file.views
import user.views
from ph_cloud import settings

admin.site.__class__ = OTPAdminSite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user.views.login_view),
    path('register/', user.views.register_view),
    path('captcha/', user.views.send_captcha_view),
    path('user/get/', user.views.get_user_view),
    path('club/', user.views.get_all_clubs),
    path('file/upload/', file.views.upload_file_view),
    path('file/get/', file.views.get_file_view),
    path('file/download/', file.views.download_file_view),
    path('files/get/', file.views.get_all_file_under_club),
    re_path('static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
