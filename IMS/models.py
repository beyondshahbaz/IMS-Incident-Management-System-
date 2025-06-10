from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    
class Role(models.Model):
    id = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 100)

class MyUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = None
    email = models.EmailField(("email address"), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] 
    objects = CustomUserManager()     
    Role = models.ForeignKey(Role, blank = True ,  on_delete = models.CASCADE, default="1")

class Department(models.Model):
    department_id = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 50)

class Employee(models.Model):
    employee_id = models.AutoField(primary_key = True)
    jobtitle = models.CharField(max_length = 50)
    contact = models.PositiveBigIntegerField(unique = True)
    Designation_id = models.ForeignKey("Designation", on_delete=models.CASCADE, related_name = "designations")
    user_id = models.OneToOneField("MyUser", on_delete=models.CASCADE, related_name = "employee")

    def __str__(self):
        return f"Employee: {self.user_id}"

class Department_poc(models.Model):
    id = models.AutoField(primary_key = True)
    department_id = models.ForeignKey(Department, on_delete = models.CASCADE  , related_name = "poccs")
    employee_id = models.ForeignKey(Employee, on_delete = models.CASCADE, related_name = "emppoc")

class Contributing_factor(models.Model):
    id = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 100)

class Incident_type(models.Model):
    id = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 100)
    department_id = models.ForeignKey(Department, on_delete = models.CASCADE)

class Designation(models.Model):
    id = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 100)
    department_id = models.ForeignKey(Department, on_delete = models.CASCADE)

class Stack_holder(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.OneToOneField("MyUser", on_delete = models.CASCADE)

class ImprovementRecommendation(models.Model):
    id = models.AutoField(primary_key = True)
    Action = models.CharField(max_length = 700, null = True)
    ResponsiblePerson = models.ForeignKey("Employee", on_delete = models.CASCADE, related_name="employee")
    incidentid = models.ForeignKey("Incident_ticket", on_delete = models.CASCADE)

class FollowupAction(models.Model):
    id = models.AutoField(primary_key = True)
    ActionTaken = models.CharField(max_length = 1000, null = True)
    DateCompleted = models.DateTimeField()
    ResponsiblePerson = models.ForeignKey("Employee", on_delete = models.CASCADE )
    incidentid = models.ForeignKey("Incident_ticket", on_delete = models.CASCADE)

class ImmediateAction(models.Model):
    id = models.AutoField(primary_key = True)
    Employeeid = models.ManyToManyField("Employee", db_table = "ImmediateActionEmployees" )
    ActionDescription = models.CharField(max_length = 2000, null = True)
    incidentid = models.ForeignKey("Incident_ticket", on_delete = models.CASCADE, null=True, related_name = "ImmediateActions")

class Severity(models.Model):
    id = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 100)

class Recurrence(models.Model):
    id = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 100)

class Risk(models.Model):
    id = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 100)

class RiskAssessment(models.Model):
    PotentialSeverity = models.ForeignKey("Severity", on_delete = models.CASCADE)
    LikehoodRecurrence = models.ForeignKey("Recurrence", on_delete = models.CASCADE)
    RiskLevel = models.ForeignKey("Risk", on_delete = models.CASCADE)
    id = models.AutoField(primary_key = True)


class Status(models.Model):
    id = models.AutoField(primary_key = True)
    Stutus = models.CharField(max_length = 20)

class StatusTime(models.Model):
    id = models.AutoField(primary_key = True)
    Date = models.DateTimeField(default = timezone.now)
    Statusid = models.ForeignKey("Status", on_delete = models.CASCADE, default = 1 )
    incidentid = models.ForeignKey("Incident_ticket", on_delete = models.CASCADE)
    

class Evidence(models.Model):
    id = models.AutoField(primary_key = True)
    File = models.FileField(upload_to = "files/", blank= True, null = True)
    incidentid = models.ForeignKey("Incident_ticket", on_delete = models.CASCADE,null = True , related_name = "EvidenceIncident")

class Incident_ticket(models.Model):
    Incidentid = models.AutoField(primary_key = True)
    Date = models.DateTimeField(auto_now = True)
    Reporter = models.ForeignKey("Employee", on_delete =  models.CASCADE)
    Incident_type = models.ForeignKey("Incident_type", null = True,on_delete=models.CASCADE)
    Location = models.CharField(max_length = 200)
    Assign_poc = models.ForeignKey("Department_poc", null = True,  on_delete = models.CASCADE, related_name = "assignpoc")
    department_id = models.ForeignKey("Department", on_delete=models.CASCADE)
    contributingfactor = models.ManyToManyField("Contributing_factor", db_table = "incident_factor")
    Individualsinvolved = models.ManyToManyField("Employee", db_table = "Individuals", null=True, related_name="Ticketindividuals") #>>>
    Witnesses = models.ManyToManyField("Employee", db_table = "Witnesstable", null=True, related_name="TicketWitnesses") #>>>
    Improvementrecommendation = models.ManyToManyField("Employee", through = "ImprovementRecommendation", null = True, related_name="TicketImprovement") #>>>
    Followupactions = models.ManyToManyField("Employee", through = "FollowupAction", null = True, related_name="TicketFollowup") #>>>
    Riskassessment = models.ForeignKey("Riskassessment", on_delete =  models.CASCADE, null = True)
    Status = models.ManyToManyField("Status", through = "StatusTime", null=True, related_name="TicketStatus")