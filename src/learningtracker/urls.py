# src/learningtracker/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyLearningViewSet, calendar_view

router = DefaultRouter()
router.register(r"daily_learning", DailyLearningViewSet, basename="daily_learning")

urlpatterns = [
    path("", calendar_view, name="calendar_view"),  # Public calendar view
    path("api/", include(router.urls)),  # API endpoints
]
