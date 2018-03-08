from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to edit an object.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if (request.user.username and
                request.method in permissions.SAFE_METHODS):
            members = obj.members.filter(user=request.user)
            if len(members):
                return True
        # Write permissions are only allowed to a superuser
        return request.user.is_superuser
