from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish_date", "status")
    list_filter = ("status", "author", "created_date", "publish_date")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title", )}
    raw_id_fields = ("author", )
    date_hierarchy = "publish_date"
    ordering = ("status", "publish_date")
