from django.contrib import admin
from social.models import Comment, Update
from django.utils.translation import gettext as _


@admin.register(Comment)
class CommentAdminForm(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('text', 'by_user', 'children',)}),
    )
    readonly_fields = ['created', ]
    filter_horizontal = ('children',)


@admin.register(Update)
class UpdateAdminForm(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('text', 'by_user', 'comments',)}),
    )
    readonly_fields = ['created', ]
    filter_horizontal = ('comments',)
