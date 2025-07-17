from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModer(permissions.BasePermission):
    """Проверка вхождения в группу moders."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class NOTModer(permissions.BasePermission):
    """Проверка не вхождения в группу moders."""

    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Проверка является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsOwnerOrModer(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.groups.filter(name="Модераторы").exists()
            or obj.owner == request.user
        )


class NOTModerOrIsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user
            and not request.user.groups.filter(name="Модераторы").exists()
        )
