from django.urls import path
from .views import CalendarEntryView, LoginView, LogoutView, get_csrf_token

urlpatterns = [
    path('api/entry/', CalendarEntryView.as_view(), name='calendar_entry'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/get-csrf-token/', get_csrf_token),
]
