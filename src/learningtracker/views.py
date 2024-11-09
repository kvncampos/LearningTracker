# src/learningtracker/views.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import DailyLearning
from .serializers import DailyLearningSerializer
from django.utils import timezone
from django.shortcuts import render
from .models import DailyLearning
from django.utils import timezone


class DailyLearningViewSet(viewsets.ModelViewSet):
    queryset = DailyLearning.objects.all()
    serializer_class = DailyLearningSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        today = timezone.now().date()
        if DailyLearning.objects.filter(date=today).exists():
            return Response(
                {"error": "An entry for today already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)


def calendar_view(request):
    """Render the calendar view with all daily learnings."""
    learnings = DailyLearning.objects.order_by("-date")
    return render(request, "home.html", {"learnings": learnings})
