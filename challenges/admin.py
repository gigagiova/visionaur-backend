from django.contrib import admin
from challenges import models
from challenges.models import ChallengeProject
from social.models import Comment
from users.models import User
from django.utils.translation import gettext as _


class UserInline(admin.TabularInline):
    model = User
    extra = 0


class ProjectInline(admin.TabularInline):
    model = ChallengeProject
    extra = 0


class CommentInline(admin.TabularInline):
    model = models.Challenge.comments.through
    extra = 0


@admin.register(models.Challenge)
class ChallengeAdminForm(admin.ModelAdmin):
    ordering = ['slug']
    list_display = ['title', 'slug', 'created']
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'description', 'image', 'organizers')}),
        (_('Important dates'), {'fields': ('created', 'deadline')}),
        (_('Applications'), {'fields': ('looking_for_team', )}),
    )
    readonly_fields = ['created', ]
    inlines = (ProjectInline, CommentInline)
    filter_horizontal = ('organizers', 'looking_for_team')
