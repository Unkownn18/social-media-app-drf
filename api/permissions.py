from rest_framework import permissions

class isPostCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        return obj.user==request.user
    
class isCommentCreator(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        return obj.user==request.user
    
class isFeedCreator(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        return False