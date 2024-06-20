from django.conf import settings

from rest_framework import permissions


class PermissionTokenIsCorrect(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.headers.get("Authorization", "") == settings.PERMISSION_TOKEN
    

class PermissionSlugIsMissing(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.kwargs.get("crm_title") in settings.SLUGS
