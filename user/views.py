import string
import random

from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _

from user import models
from user.forms import LoginForm, RegisterForm, EmailForm
from user.models import User, Club


def user_dump(user: models.User):
    return {
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'last_login': str(user.last_login),
    }


def clubs_dump(clubs: [models.Club]):
    return [{
        'club_id': club.club_id,
        'club_name': club.club_name,
        'owner_email': club.owner_email
    } for club in clubs]


@csrf_exempt
def login_view(request):
    if not request.method == 'POST':
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)

    form = LoginForm(request.POST)

    if not form.is_valid():
        return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(username=username, password=password)

    if not user:
        return JsonResponse({'status': 'error', 'message': _('Invalid Credentials')}, status=401)

    user = User.objects.get(user_name=username)
    if user.is_superuser:
        return JsonResponse({'status': 'success', 'message': _('You can not login as a superuser')},
                            status=401)

    login(request, user)
    request.session['user_id'] = user.user_id
    return JsonResponse({'status': 'success', 'message': _('Login Successful')})


@csrf_exempt
def register_view(request):
    if not request.method == 'POST':
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)

    form = RegisterForm(request.POST)

    if not form.is_valid():
        return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    user_name = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    email = form.cleaned_data.get('email')
    user = User.objects.create_user(user_name, password, email)
    user.save()

    return JsonResponse({'status': 'success', 'message': _('Registration Successful')})


def send_captcha_view(request):
    if not request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)

    form = EmailForm(request.GET)

    if not form.is_valid():
        return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    email = form.cleaned_data.get('email')
    captcha = ''.join(random.sample(string.ascii_letters + string.digits, 5))
    cache.set(email, captcha, 600 * 5)
    send_mail(
        _('Desert Captcha'),
        captcha,
        'luo_evan@163.com',
        [email],
        fail_silently=True,
    )
    return JsonResponse({'status': 'success', 'message': _('Captcha Sent')})


def get_user_view(request):
    if not request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)

    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    return JsonResponse({'status': 'success', 'data': user_dump(user)})


def get_all_clubs(request):
    if not request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)

    return clubs_dump(Club.objects.all())
