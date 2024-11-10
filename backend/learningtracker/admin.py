from django.contrib import admin

# Register your models here.
from .models import DailyLearning


@admin.register(DailyLearning)
class DailyLearningAdmin(admin.ModelAdmin):
    list_display = ["date", "description"]
    ordering = ["-date"]
