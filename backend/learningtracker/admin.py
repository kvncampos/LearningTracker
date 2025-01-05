from django.contrib import admin

# Register your models here.
from .models import DailyLearning, Tag


@admin.register(DailyLearning)
class DailyLearningAdmin(admin.ModelAdmin):
    list_display = ["date", "description", "learning_type", "user"]
    ordering = ["-date"]
    list_filter = ["learning_type", "tags", "date"]
    search_fields = ["description", "tags__name", "user__username"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "user")  # Show tag name and user in the admin list
    search_fields = ["name", "user__username"]  # Enable search by tag name and user
    list_filter = ["user"]  # Filter by user
