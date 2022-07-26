from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

from file.forms import FileUploadForm, GetFileForm, GetAllFilesUnderClubForm
from file.models import FileInfo
from user.models import User, Club


def file_dump(file: FileInfo):
    return {
        'file_id': file.file_id,
        'club_id': file.club_id,
        'created_at': file.created_at,
        'file_url': file.file.url
    }


def files_dump(files: [FileInfo]):
    return [
        file_dump(file)
        for file in files
    ]


@csrf_exempt
def upload_file_view(request):
    if not request.method == 'POST':
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)

    form = FileUploadForm(request.POST, request.FILES)

    if not form.is_valid():
        return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)

    user_id = request.session.get('user_id')
    email = User.objects.get(user_id=user_id).email
    club_id = form.clean_club_id()
    file_name = form.cleaned_data.get('file_name')

    if not Club.objects.filter(email=email, club_id=club_id).exists():
        return JsonResponse({'status': 'error', 'message': _('Club is not existed')}, status=404)

    with open(r'club/' + club_id + '/' + file_name, 'wb') as f:
        for chunk in request.FILES.get('file'):
            f.write(chunk)
        f.close()
    return JsonResponse({'status': 'success', 'message': _('Upload Successful')})


def get_file_view(request):
    if not request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)

    form = GetFileForm(request.GET)

    if not form.is_valid():
        return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    file_id = form.clean_file_id()
    return JsonResponse({'status': 'success', 'data': file_dump(FileInfo.objects.get(file_id=file_id))})


def download_file_view(request):
    if not request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)

    form = GetFileForm(request.GET)

    if not form.is_valid():
        return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    file_id = form.clean_file_id()
    file_url = FileInfo.objects.get(file_id=file_id).file.url
    redirect(file_url)


def get_all_file_under_club(request):
    if not request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)

    form = GetAllFilesUnderClubForm(request.GET)

    if not form.is_valid():
        return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    club_id = form.clean_club_id()
    return JsonResponse({'status': 'success', 'data': files_dump(FileInfo.objects.filter(club_id=club_id))})
