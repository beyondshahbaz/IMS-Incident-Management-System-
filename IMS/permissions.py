from rest_framework.permissions import BasePermission

class Rolepermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.Role.Name == "POC" and request.method in ["GET","POST","PUT"]:
            return True
        if request.user.Role.Name == "Employee" and request.method in ["GET","POST"]:
            return True
        if request.user.Role.Name == "Stake Holder" and request.method in ["GET"]:
            return True

        return False