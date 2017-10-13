from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsManager(permissions.BasePermission):
    message = 'Allowed only for manager'

    def has_permission(self, request, view):
        return 'ShopManager' in [i.name for i in request.user.groups.all()]


