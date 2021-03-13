from pprint import pprint
from rest_framework import permissions


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class IsConnectorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_connector == True


# SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsTicketOwnerYOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner
