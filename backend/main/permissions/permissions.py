from rest_framework import permissions


class IsAuthenticatedAndOwner(permissions.BasePermission):
    message = 'You must be the owner of this object.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthenticatedAndProfileOwner(permissions.BasePermission):
    message = 'You must be the owner of the Profile.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.profile == request.user.profile
