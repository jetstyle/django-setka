from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse

# from ..models import AdvancedArticle


class SetkaArticle(admin.ModelAdmin):
    fields = ('title', 'content', 'setla_layout_id', 'setka_theme_id',)
    list_display = ('title', 'setkaarticle_preview',)
    change_form_template = 'admin_templates/change_form.html'
    change_list_template = 'admin_templates/change_list.html'

    def setkaarticle_preview(self, obj):
        return format_html('<a class="button stkbtn" href="{}">Preview</a>',
                           reverse('setka:article-preview', args=[obj.pk]))

    setkaarticle_preview.short_description = 'Preview'


# @admin.register(AdvancedArticle)
class SetkaAdvancedArticle(SetkaArticle):
    list_display = ('title', 'setkaarticle_preview', 'setkaarticle_drafts', 'setkaarticle_publishing')

    def setkaarticle_drafts(self, obj):
        return format_html('<a class="button stkbtn" href="{}">Drafts</a>',
                           reverse('setka:article-drafts', args=[obj.pk]))

    def setkaarticle_publishing(self, obj):
        if not hasattr(obj, 'setkapublished'):
            return format_html('<button class="button setkapost stkbtn" value="{}">Publish</button>',
                               reverse('setka:article-publish', args=[obj.pk]))

        return format_html('<a class="button" href="{}" target="_blank">Preview</a>&nbsp;'
                           '<button class="button setkapost stkbtn" value="{}">Update</button>'
                           '<button class="button setkapost stkbtn" value="{}">Load</button>'
                           '<button class="button setkapost stkbtn" value="{}">Unpublish</button>&nbsp;',
                           reverse('setka:published-preview', args=[obj.pk]),
                           reverse('setka:article-publish', args=[obj.pk]),
                           reverse('setka:published-load', args=[obj.pk]),
                           reverse('setka:article-unpublish', args=[obj.pk]))

    setkaarticle_drafts.short_description = 'Draft pages'
    setkaarticle_publishing.short_description = 'Publishing'
