from django.conf import settings


def setka_token(request):
    return {'SETKA_PUBLIC_TOKEN': settings.SETKA_PUBLIC_TOKEN}
