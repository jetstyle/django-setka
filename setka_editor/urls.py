from django.conf.urls import url
from .views import ArticleViews, SetkaImagesView, update_files, Published, Draft

app_name = 'setka'
urlpatterns = [
    url(r'^article/(?P<article_id>\d+)/published_preview$', Published.preview_published, name='published-preview'),
    url(r'^article/(?P<article_id>\d+)/published_load$', Published.load_published, name='published-load'),

    url(r'^article/(?P<article_id>\d+)/preview$', ArticleViews.preview, name='article-preview'),
    url(r'^article/(?P<article_id>\d+)/publish$', ArticleViews.publish, name='article-publish'),
    url(r'^article/(?P<article_id>\d+)/unpublish$', ArticleViews.unpublish, name='article-unpublish'),
    url(r'^article/(?P<article_id>\d+)/drafts$', ArticleViews.get_drafts, name='article-drafts'),

    url(r'^draft/(?P<draft_id>\d+)/preview$', Draft.preview, name='draft-preview'),
    url(r'^draft/(?P<draft_id>\d+)/delete$', Draft.delete, name='draft-delete'),
    url(r'^draft/(?P<draft_id>\d+)/load$', Draft.load, name='draft-load'),

    url(r'^api/images', SetkaImagesView.as_view(), name='images'),

    url(r'^api/update', update_files, name='sync')
]
