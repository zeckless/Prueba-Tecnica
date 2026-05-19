from django.contrib import admin

from .models import Discussion, PromptActivity, Resource


@admin.register(PromptActivity)
class PromptActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "level", "author", "status", "likes")
    list_filter = ("status", "subject", "level")
    search_fields = ("title", "summary", "prompt", "author", "tags")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "resource_type", "source", "featured")
    list_filter = ("resource_type", "featured")
    search_fields = ("title", "description", "source")


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "author", "replies", "last_activity")
    list_filter = ("topic",)
    search_fields = ("title", "body", "author")
