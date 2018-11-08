from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class IsSelfOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow owners or admin of an object to edit or retrieve / list  it.
    """
    message = 'This is not your asset nor you are and Admin'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.user.email == obj.email
