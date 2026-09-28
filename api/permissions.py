from rest_framework.permissions import BasePermission
from .models import Company
class IsAdminUser(BasePermission):
    message='Admin role required.'
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user,'company') and request.user.company.role == Company.Role.ADMIN)
