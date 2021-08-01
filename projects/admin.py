from django.contrib import admin
from django import forms

from projects import models
from django.utils.translation import gettext as _


class UserInline(admin.TabularInline):
    model = models.UserProject
    extra = 0


@admin.register(models.Project)
class ProjectAdminForm(admin.ModelAdmin):
    ordering = ['slug']
    list_display = ['title', 'slug', 'created']
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'description', 'category', 'stage', 'image',)}),
        (_('Important dates'), {'fields': ('created',)}),
        (_('Applications'), {'fields': ('looking_for', 'skills_needed')})
    )
    readonly_fields = ['created', ]
    inlines = (UserInline, )
    filter_horizontal = ('skills_needed',)
