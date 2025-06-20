from django.contrib import admin
from django.urls import path ,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter





router = DefaultRouter()
router.register(r"incident", TicketViewSet)
router.register(r"employee", EmployeeViewSet)
router.register(r"department", DepartmentViewSet)
router.register(r"incidenttype", IncidentTypeViewSet)
router.register(r"designation", DesignationViewSet)
router.register(r"role", RoleViewSet)
router.register(r"deppoc", DepartmentPOCViewSet)
router.register(r"contributingf", ContributingFactorsViewSet)
router.register(r"status", StatusViewSet)
router.register(r"updatestatus", StatusUpdateViewSet, basename="Update_Status")
router.register(r"poc", PocTicketViewSet, basename="Poc_Update")



urlpatterns = [
    path("", include(router.urls)),
    path('login/', Login.as_view(), name='custom_login'),
    path("logout/",LogoutView.as_view(), name = "custom_logout"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("resetpassword/", ResetPassword.as_view(), name = "resetpassword"),
    path("forgetpassword/",Forgetpassword.as_view(), name = "forgetpassword"),
    path("varifypassword/",varify_password.as_view(), name = "varifyPassword"),
    path("newpassword/", NewPassword.as_view(), name = "varifiedNewPassword"),
] + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
