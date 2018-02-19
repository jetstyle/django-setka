import json

from django.db import models
from django.forms import model_to_dict
from django.core.exceptions import ObjectDoesNotExist


class Article(models.Model):
    title = models.CharField('Title', max_length=255)
    pub_date = models.DateTimeField('Publication date', blank=True, null=True, editable=False)
    content = models.TextField('Content')
    setka_theme_id = models.CharField(max_length=255)
    setla_layout_id = models.CharField(max_length=255)

    template = 'pages/preview_page.html'

    def __str__(self):
        return '{}--{}'.format(self.id, self.title)


class AdvancedArticle(Article):
    """
    Such articles has drafts and published version.
    """

    def open_draft(self, dump):
        self.__dict__.update(json.loads(dump))
        self.save()

    def publish(self):
        data = model_to_dict(self)
        del data['id']
        dump = json.dumps(data)
        try:
            self.setkapublished.dump = dump
            self.setkapublished.save()
        except ObjectDoesNotExist:
            SetkaPublished(article=self, dump=dump).save()

    def unpublish(self):
        if not hasattr(self, 'setkapublished'):
            return

        published = self.setkapublished
        SetkaDraft(article=published.article, dump=published.dump).save()
        published.delete()

    def save_revision(self):
        data = model_to_dict(self)
        del data['id']
        SetkaDraft(name=self.title, article=self, dump=json.dumps(data)).save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id:
            self.save_revision()
        super().save(force_insert, force_update, using, update_fields)


class SetkaDraft(models.Model):
    name = models.CharField('Title', max_length=255)
    article = models.ForeignKey(AdvancedArticle)
    created_at = models.DateTimeField(auto_now_add=True)
    dump = models.TextField()

    def __str__(self):
        return '{}--{}'.format(self.name, self.created_at.strftime('%H:%M:%S %d.%m.%Y'))

    class Meta:
        ordering = ['-created_at']


class SetkaPublished(models.Model):
    article = models.OneToOneField(AdvancedArticle)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    dump = models.TextField()

    def __str__(self):
        return '{}--{}--{}'.format(self.article.title, self.created_at.strftime('%H:%M:%S %d.%m.%Y'),
                                   self.last_modified.strftime('%H:%M:%S %d.%m.%Y'))

    class Meta:
        ordering = ['-created_at']


class ImageDocument(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=50, unique=True)
    alt = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '{}'.format(self.id)
