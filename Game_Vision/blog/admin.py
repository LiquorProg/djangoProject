from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'created_at')
    list_display_links = ('id', 'text')
    search_fields = ('text', 'author',)
    # prepopulated_fields = {"slug": ("name",)}

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, admin.ModelAdmin)