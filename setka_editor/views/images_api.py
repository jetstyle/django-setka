import os
import json
from slugify import slugify

from django.http import JsonResponse
from django.views.generic import View
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import permission_required

from ..models import ImageDocument


def _build_image_url(slug):
    return '/media/images/{}'.format(slug)


class SetkaImagesView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(permission_required('is_stuff', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(SetkaImagesView, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def get(request, *args, **kwargs):
        images = ImageDocument.objects.all().order_by('-id')
        data = [{
            'id': image.slug,
            'name': image.name,
            'url': request.build_absolute_uri(_build_image_url(image.slug)),
            'thumbUrl': request.build_absolute_uri(_build_image_url(image.slug)),
            'alt': image.alt if image.alt else ''
        } for image in images]
        return JsonResponse({'postimages': data}, status=200)

    @staticmethod
    def post(request, *args, **kwargs):
        temp = request.FILES['file']
        name = temp.name
        slug = '{}.{}.{}'.format(slugify(name, max_length=50), '0', name.split('.')[-1])

        # checking for copies
        existing = [x[0] for x in ImageDocument.objects.values_list('slug')]
        copy_count = 1
        while slug in existing:
            slug_elems = slug.split('.')
            slug_elems[-2] = '.' + str(copy_count)
            slug = '.'.join(slug_elems)
            copy_count += 1

        try:
            ImageDocument(name=name, slug=slug).save()
            with default_storage.open(os.path.join('images', slug), 'wb+') as dest:
                for chunk in temp.chunks():
                    dest.write(chunk)
            return JsonResponse({'id': slug, 'url': _build_image_url(slug)})
        except IntegrityError:
            return JsonResponse({}, status=500)

    @staticmethod
    def delete(request, *args, **kwargs):
        slug = request.path.split('/')[-1]
        try:
            ImageDocument.objects.get(slug=slug).delete()
        except ImageDocument.DoesNotExist:
            return JsonResponse({}, status=404)

        path = os.path.join('images', slug)
        if default_storage.exists(path):
            default_storage.delete(path)
        return JsonResponse({}, status=200)

    @staticmethod
    def put(request, *args, **kwargs):
        slug = request.path.split('/')[-1]
        try:
            image = ImageDocument.objects.get(slug=slug)
        except ImageDocument.DoesNotExist:
            return JsonResponse({}, status=404)

        data = json.loads(request.body)
        if 'alt' in data:
            image.alt = data['alt']
        if 'name' in data:
            image.name = data['name']
        image.save()
        return JsonResponse({}, status=200)
