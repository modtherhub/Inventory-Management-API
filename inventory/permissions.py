from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
        """only the owner of the item (or implicitly an administrator via a queryset) is allowed to access the object"""
        def has_object_permission(self, request, view, obj):
            return getattr(obj, 'owner_id', None) == request.user.id or request.user.is_staff


class IsSelfOrAdmin(BasePermission):
    """user manages their own data, or an administrator manages everyone"""
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.id == request.user.id


    def has_permission(self, request, view):
        return True