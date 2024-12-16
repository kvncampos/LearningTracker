from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from .views import DailyLearningViewSet, LoginView, LogoutView, get_csrf_token

# Create a router and register your ViewSet
router = DefaultRouter()
router.register(r"learned-entries", DailyLearningViewSet, basename="daily-learning")

# Define your urlpatterns
urlpatterns = [
    # Schema generation endpoint
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # ReDoc
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/get-csrf-token/", get_csrf_token, name="get-csrf-token"),
    path("", include(router.urls)),
]
