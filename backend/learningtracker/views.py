from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from .models import DailyLearning
from .permissions import IsAuthenticatedOrReadOnly
from datetime import date
from django.http import JsonResponse

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'message': 'CSRF token set'})

class CalendarEntryView(APIView):
    def get(self, request):
        selected_date = request.query_params.get('date', date.today().strftime('%Y-%m-%d'))
        entry = DailyLearning.objects.filter(date=selected_date).first()
        description = entry.description if entry else "No Entries Yet, Go out and Learn something New!"
        return Response({'description': description})

class LoginView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Logged in successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class EntryView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        date = request.GET.get('date')
        if date:
            try:
                entry = DailyLearning.objects.get(date=date)
                return Response({"description": entry.description}, status=status.HTTP_200_OK)
            except DailyLearning.DoesNotExist:
                return Response({"description": "No entry found for this date."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        date = request.data.get('date')
        description = request.data.get('description')
        if date and description:
            entry, created = DailyLearning.objects.get_or_create(date=date, defaults={'description': description})
            if not created:
                entry.description = description
                entry.save()
            return Response({"message": "Entry saved successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Date and description are required."}, status=status.HTTP_400_BAD_REQUEST)
