from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to allow GET requests for everyone,
    but require authentication for POST, PUT, DELETE requests.
    """
    def has_permission(self, request, view):
        # Allow GET requests for everyone
        if request.method in SAFE_METHODS:
            return True
        # Require authentication for other methods
        return request.user and request.user.is_authenticated
