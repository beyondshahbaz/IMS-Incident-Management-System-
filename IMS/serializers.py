from rest_framework import serializers
from IMS.models import *
from time import timezone

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
        
class ImprovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprovementRecommendation
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
        
class RiskAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAssessment
        fields = "__all__"

class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = "__all__"

class TicketSerializer(serializers.ModelSerializer):
    ImmediateActions = ImmediateActionSerializer(many = True)
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
        
        
        return Ticket
            


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
        
        
        
        
        
            
class PocTicketSerializer(serializers.ModelSerializer):
    Improvementrecommendation = ImprovementSerializer(many=True ,write_only=True)
    # Followupactions = FollowupSerializer(many = True) 
    # Riskassessment = RiskAssessmentSerializer(many = True)


    class Meta:
        model = Incident_ticket
        fields = ["Incidentid","Improvementrecommendation"] #,"Followupactions","Riskassessment"]
    
    
    def update(self, instance, validated_data):
        
        Impovement_list = validated_data.pop("Improvementrecommendation")   
        print(Impovement_list)
        for objectss in Impovement_list:
            print(objectss)
            
            objectss["incidentid"] = instance
            
            #  --- Object Creation
            ImprovementRecommendationss = ImprovementRecommendation.objects.create(**objectss)
            
            
        return instance

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        