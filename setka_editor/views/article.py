import json

from django.http import HttpResponse, JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from ..utils import update_setka_build, staff_and_certain_method_required
from ..models import SetkaDraft, Article, AdvancedArticle


class ArticleViews:
    @staticmethod
    @staff_and_certain_method_required(['GET'])
    def preview(request, article_id):
        try:
            article = Article.objects.get(id=article_id)
            return render(request, article.template, {'content': article.content})
        except Article.DoesNotExist:
            raise Http404()

    @staticmethod
    @staff_and_certain_method_required(['GET'])
    def get_drafts(request, article_id):
        try:
            drafts = SetkaDraft.objects.filter(article=Article.objects.get(id=article_id)).order_by('-created_at')
            data = [{'name': str(x), 'id': x.id} for x in drafts]
            return render(request, 'pages/draft_list.html', {'drafts': data})
        except Article.DoesNotExist:
            raise Http404()

    @staticmethod
    @staff_and_certain_method_required(['POST'])
    def publish(request, article_id):
        try:
            AdvancedArticle.objects.get(id=article_id).publish()
            return JsonResponse({}, status=200)
        except AdvancedArticle.DoesNotExist:
            raise JsonResponse({}, status=404)

    @staticmethod
    @staff_and_certain_method_required(['POST'])
    def unpublish(request, article_id):
        try:
            AdvancedArticle.objects.get(id=article_id).unpublish()
            return JsonResponse({}, status=200)
        except AdvancedArticle.DoesNotExist:
            raise JsonResponse({}, status=404)


class Draft:
    @staticmethod
    @staff_and_certain_method_required(['POST'])
    def load(request, draft_id):
        try:
            draft = SetkaDraft.objects.get(id=draft_id)
            draft.article.open_draft(draft.dump)
            return JsonResponse({}, status=200)
        except (SetkaDraft.DoesNotExist, ObjectDoesNotExist):
            return JsonResponse({}, status=404)

    @staticmethod
    @staff_and_certain_method_required(['DELETE'])
    def delete(request, draft_id):
        try:
            SetkaDraft.objects.get(id=draft_id).delete()
            return JsonResponse({}, status=200)
        except SetkaDraft.DoesNotExist:
            return JsonResponse({}, status=404)

    @staticmethod
    @staff_and_certain_method_required(['GET'])
    def preview(request, draft_id):
        try:
            draft = SetkaDraft.objects.get(id=draft_id)
            article = json.loads(draft.dump)
            return render(request, draft.article.template, article)
        except SetkaDraft.DoesNotExist:
            raise Http404


class Published:
    @staticmethod
    @staff_and_certain_method_required(['POST'])
    def load_published(request, article_id):
        try:
            article = AdvancedArticle.objects.get(id=article_id)
        except AdvancedArticle.DoesNotExist:
            return JsonResponse({}, status=404)

        if hasattr(article, 'setkapublished'):
            article.open_draft(article.setkapublished.dump)
            return JsonResponse({}, status=200)

        return JsonResponse({}, status=404)

    @staticmethod
    @staff_and_certain_method_required(['GET'])
    def preview_published(request, article_id):
        try:
            article = AdvancedArticle.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise Http404()

        if hasattr(article, 'setkapublished'):
            return render(request, article.template, json.loads(article.setkapublished.dump))

        raise Http404()


def update_files(request):
    update_setka_build()
    return HttpResponse(status=200)
