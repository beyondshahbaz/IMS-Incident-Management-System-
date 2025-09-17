from rest_framework import serializers
from IMS.models import *
from time import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['employee_id'] = user.employee.employee_id

        return token


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["first_name","last_name","email","password","Role"]

class EmployeeSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    
    class Meta:
        model = Employee
        fields = '__all__'

    #  ---Validate data contains user input
    def create(self, validated_data):
        
        Password = validated_data["user_id"].pop("password")
        
        # ---User Creation
        Userobj = MyUser.objects.create(
            **validated_data.pop("user_id")
        )
        Userobj.set_password(Password)
        Userobj.save()
        
        #Emplyee Creation
        employee = Employee.objects.create(
            user_id = Userobj,
            **validated_data
        )
        employee.save()
        
        return employee
    
        
class Incident_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident_type
        fields = '__all__'

class Contributing_factorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributing_factor
        fields = '__all__'

class Department_pocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department_poc
        fields = '__all__'

class StakeHolderSerializer(serializers.ModelSerializer):
    class Meta:
        models = Stack_holder
        fields = "__all__"

        
class FollowupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowupAction
        fields = ["ActionTaken","ResponsiblePerson"]

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"
        
class StatusTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusTime
        fields = "__all__"

class ImmediateActionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImmediateAction
        fields = "__all__"
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        idd = data.pop("id")
        tokenid = data.pop("incidentid")
        data["Employeeid"] = [ 
            i["user_id"]["first_name"] + " " + i["user_id"]["last_name"] for i in EmployeeSerializer(instance.Employeeid , many=True).data ]
        return data
    # --- DONE*******************************
    
class ImprovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprovementRecommendation
        fields = "__all__"
    
    # def to_representation(self, instance):
    #     dataa = super().to_representation(instance)
    #     idd = dataa.pop("id")
    #     # incidentid = dataa.pop("Incidentid")
    #     dataa["employee_id"] = instance.employee_id.user_id.first_name + " " + instance.employee_id.user_id.last_name
    #     return dataa


class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = "__all__"

class TicketSerializer(serializers.ModelSerializer):
    ImmediateActions = ImmediateActionSerializer(many = True)
    # ImprovementRecommendation = ImprovementSerializer(many = True)
    Status = StatusSerializer( many = True, read_only = True)
    
    class Meta:
        model = Incident_ticket
        fields = "__all__"
    
    
    def create(self, validated_data):
        
        DepartmentID = validated_data["department_id"]
        
        ContributingFactor = validated_data.pop("contributingfactor")
        Individuals = validated_data.pop("Individualsinvolved")
        Witness = validated_data.pop("Witnesses")
        Pocc = validated_data.pop("Assign_poc")
        Action = validated_data.pop("ImmediateActions")
        # Action = validated_data.pop("Improvementrecommendation")
        
        
        #  ---POC Assign
        POC = DepartmentID.poccs.first()
        validated_data["Assign_poc"] = POC
        
        #  ---Ticket Creation
        Ticket = Incident_ticket.objects.create(
            **validated_data 
        )
        
        Ticket.Status.set([Status.objects.get(id = 1)])
        
        #  ---LOOP FOR GETTING EVERY ACTION
        for objectss in Action:
            
            #  ---EXTRACTING EMPLOYEES FROM IMMEDIATEACTION 
            employees = objectss.pop("Employeeid")
            objectss["incidentid"] = Ticket
            
            #  ---CREATING IMMEDIATEACTION OBJECT
            ImmediateActionobject = ImmediateAction.objects.create(
                    **objectss)
            
            #  ---INITIALIZING EMPLOYEES TO IMMEDIATEACTION
            ImmediateActionobject.Employeeid.set(employees)
        
        
        # ---MANY TO MANY FIELDS ASSIGN
        for i in ContributingFactor:
            Ticket.contributingfactor.add(i)

        for i in Individuals:
            Ticket.Individualsinvolved.add(i)

        for i in Witness:
            Ticket.Witnesses.add(i)
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        depar = data.pop("department_id")
        ppp = data.pop("Assign_poc")
        Incidentid = data.pop("Incidentid")
        ccc = data.pop("contributingfactor")
        
        data["Ticket_id"] = Incidentid
        data["Reporter"] ={
            "Name": instance.Reporter.user_id.first_name + " " + instance.Reporter.user_id.last_name ,
            "Designation": instance.Reporter.Designation_id.Name,
    }
        data["Incident_type"] = instance.Incident_type.Name

        data["Department"]= {
            "id": instance.department_id.department_id ,
            "Name" : instance.department_id.Name ,
    }
        if instance.Assign_poc is not None : 
            data ["Assign_poc"]= {
        "Name": instance.Assign_poc.employee_id.user_id.first_name + " " + instance.Assign_poc.employee_id.user_id.last_name
    },
        else:
            data ["Assign_poc"]= ""

        data ["Contributingfactor"] = [ 
            i["Name"] for i in Contributing_factorsSerializer(instance.contributingfactor , many=True).data ]
        
        data ["Individualsinvolved"] = [ 
            i["user_id"]["first_name"] + " " + i["user_id"]["last_name"] for i in EmployeeSerializer(instance.Individualsinvolved , many=True).data ]
        
        data ["Witnesses"] = [ 
            i["user_id"]["first_name"] + " " + i["user_id"]["last_name"] for i in EmployeeSerializer(instance.Witnesses , many=True).data ]
             
        data["Improvementrecommendation"] = [ 
                                             {
                                                 "id":ir.id,
                                                "Action" : ir.Action ,
                                                "employee_id" : ir.employee_id.user_id.id,
                                                "employee" : ir.employee_id.user_id.first_name + " " + ir.employee_id.user_id.last_name ,
                                                "Incidentid" : ir.Incidentid.Incidentid
                                             
                                             } for ir in instance.TikectRecommendation.all()]
        
        data["Followupactions"] = [
            {
                "id" : fw.id ,
                "ActionTaken" :fw.ActionTaken,
                "DateCompleted" : fw.DateCompleted,
                "ResponsiblePerson" : fw.ResponsiblePerson.user_id.id,
                "incidentid" : fw.incidentid.Incidentid
                
            }   for fw in instance.Followup.all()
        ]
        
        data["Status"] = [
            {
                "Name" : i.Statusid.Stutus,
                "Date" : i.Date
            }   for i in instance.Statuss.all()
        ]
        
        # # data["SeverityLevel"] = instance.SeverityLevel.Name
        # data["Recurrence"] = instance.Recurrence.Name
        # data["Risk"] = instance.Risk.Name
        return data
            


class StatusUpdate(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only = True)
    
    class Meta:
        model = Incident_ticket
        fields = ["Incidentid","id"]
    
    def update(self, instance, validated_data):
        
        statusid = validated_data.pop("id")
        
        StatusTime.objects.create(
            incidentid = instance,
            Statusid = Status.objects.get(pk = statusid )
        )
        
        return instance
        

# --- Assign POC work !!
class PocTicketSerializer(serializers.ModelSerializer):
    Improvementrecommendation = ImprovementSerializer(many=True , write_only=True)
    Followupactions = FollowupSerializer(many = True)


    class Meta:
        model = Incident_ticket
        fields = ["Incidentid","Improvementrecommendation","Followupactions"]
    
    
    def update(self, instance, validated_data):
        
        Impovement_list = validated_data.pop("Improvementrecommendation")   
        FollowupActions = validated_data.pop("Followupactions")
        
        for objectss in Impovement_list:
        
            objectss["incidentid"] = instance
            
            #  --- Object Creation ---
            ImprovementRecommendationss = ImprovementRecommendation.objects.create(**objectss)
          
        
        for actions in FollowupAction:
            
            actions["incidentid"] = instance
            
            # --- object Creation
            FollowupActionss = FollowupAction.objects.create(**actions)
            
        return instance



        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
         