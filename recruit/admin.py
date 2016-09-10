from django.contrib import admin
from .models import Comment, Post, Participation


class CommentInline(admin.StackedInline):
    model = Comment


class ParticipationInline(admin.StackedInline):
    model = Participation


class PostAdmin(admin.ModelAdmin):
    inline = (CommentInline, ParticipationInline)
    list_display = ('title', 'author', 'registered_date')

admin.site.register(Post, PostAdmin)

