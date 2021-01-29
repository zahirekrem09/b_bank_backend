from rest_framework import permissions


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class IsConnectorUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_connector == True
