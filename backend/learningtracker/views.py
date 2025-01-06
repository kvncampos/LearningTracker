import logging

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.openapi import AutoSchema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import DailyLearningFilter, TagFilter
from .models import DailyLearning, Tag
from .serializers import DailyLearningSerializer, TagSerializer

logger = logging.getLogger(__name__)


class WelcomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                "message": "Welcome to the Learning Tracker API!",
                "info": "Use the API to manage your learning entries. Frontend is powered by React.",  # noqa: E501
            }
        )


class DailyLearningViewSet(ModelViewSet):
    queryset = DailyLearning.objects.all()
    serializer_class = DailyLearningSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DailyLearningFilter
    schema = AutoSchema()

    def get_queryset(self):
        return (
            self.queryset.filter(
                user=self.request.user
            )  # Fetch entries for the logged-in user only.
            .select_related(
                "user"
            )  # Optimize database queries by joining the "user" table.
            .order_by("date")  # Sort results by date.
        )

    def perform_create(self, serializer):
        logger.info(f"User {self.request.user} is creating an entry.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        logger.info(f"User {self.request.user} updated an entry.")
        serializer.save()


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TagFilter
    schema = AutoSchema()

    def get_queryset(self):
        return (
            self.queryset.filter(
                user=self.request.user
            )  # Fetch entries for the logged-in user only.
            .select_related(
                "user"
            )  # Optimize database queries by joining the "user" table.
            .order_by("name")  # Sort results by name.
        )

    def perform_create(self, serializer):
        logger.info(f"User {self.request.user} is creating a tag.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        logger.info(f"User {self.request.user} updated a tag.")
        serializer.save()


@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)  # Fetch the CSRF token directly
    return JsonResponse(
        {
            "message": "CSRF token set",
            "csrfToken": csrf_token,  # Include the CSRF token in the response
        }
    )


class LoginView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        # Log a warning if the CSRF token is missing or invalid
        if "X-CSRFToken" not in request.headers:
            logger.warning("CSRF token missing or invalid in login request.")

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            logger.info(f"User {username} logged in successfully.")
            return Response(
                {"message": "Logged in successfully"}, status=status.HTTP_200_OK
            )
        logger.warning(f"Failed login attempt for username: {username}")
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )
