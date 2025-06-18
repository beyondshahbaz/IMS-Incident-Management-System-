from django.contrib import admin
from IMS.models import *
# Register your models here.

admin.site.register(Incident_ticket)
admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Department_poc)
admin.site.register(Designation)
admin.site.register(Contributing_factor)
admin.site.register(Incident_type)
admin.site.register(MyUser)
admin.site.register(Severity)
admin.site.register(Recurrence)
admin.site.register(Risk)
admin.site.register(ImmediateAction)
admin.site.register(Evidence)
admin.site.register(Status)
admin.site.register(ImprovementRecommendation)
admin.site.register(FollowupAction)
admin.site.register(StatusTime)