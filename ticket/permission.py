from rest_framework import permissions
from pprint import pprint


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request in permissions.SAFE_METHODS:
            return True
        pprint(request.user)
        pprint(obj.owner)
        return request.user.id == obj.owner.id
