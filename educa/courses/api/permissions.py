from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    def has_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()