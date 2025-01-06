from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from .views import (
    DailyLearningViewSet,
    LoginView,
    LogoutView,
    TagViewSet,
    WelcomeView,
    get_csrf_token,
)

# Create a router and register your ViewSets
router = DefaultRouter()
router.register(r"learned-entries", DailyLearningViewSet, basename="daily-learning")
router.register(r"tags", TagViewSet, basename="tag")  # Register TagViewSet

# Define your urlpatterns
urlpatterns = [
    # Public Welcome Page
    path("", WelcomeView.as_view(), name="welcome"),
    # API Schema Endpoints
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Authentication and CSRF
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/csrf/", get_csrf_token, name="get-csrf-token"),
    # Registered API Routes
    path("api/", include(router.urls)),  # Prefix all API routes with /api/
]
