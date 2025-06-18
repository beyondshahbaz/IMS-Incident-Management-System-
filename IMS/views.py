from django.shortcuts import render
from .models import *
from rest_framework.decorators import *
from rest_framework.response import Response 
from rest_framework import serializers
from IMS.serializers import *
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from rest_framework.views import APIView 
from rest_framework.decorators import api_view , authentication_classes , permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from IMS.permissions import *
from rest_framework import viewsets
from django.http import HttpResponseRedirect



class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    
class DepartmentPOCViewSet(viewsets.ModelViewSet):
    queryset = Department_poc.objects.all()
    serializer_class = Department_pocSerializer

class IncidentTypeViewSet(viewsets.ModelViewSet):
    queryset = Incident_type.objects.all()
    serializer_class = Incident_typeSerializer

class ContributingFactorsViewSet(viewsets.ModelViewSet):
    queryset = Contributing_factor.objects.all()
    serializer_class = Contributing_factorsSerializer

class StakeHolderViewSet(viewsets.ModelViewSet):
    queryset = Stack_holder.objects.all()
    serializer_class = StakeHolderSerializer
    
class TicketViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, Rolepermissions]
    # authentication_classes = [JWTAuthentication]
    queryset = Incident_ticket.objects.all()
    serializer_class = TicketSerializer
    
    
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class StatusUpdateViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, Rolepermissions]
    # authentication_classes = [JWTAuthentication]
    queryset = Incident_ticket.objects.all()
    serializer_class = StatusUpdate
    
class PocTicketViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, Rolepermissions]
    # authentication_classes = [JWTAuthentication]
    queryset = Incident_ticket.objects.all()
    serializer_class = PocTicketSerializer


    
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email,password)
        
        user = authenticate(email = email, password = password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                'access token': str(refresh.access_token),
                'refresh token': str(refresh),
            })
        else:
            return Response({'error': 'Invalid email or password'}, status = status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
        
        
class ResetPassword(APIView):
    def post(self, request):
        try:
            givendata = request.data
            email = givendata.get('email')
            password = givendata.get('password')
            newpassword = givendata.get('newpassword')
        
            user = authenticate(email = email, password = password)
            
            if user is not None:
                userdata = MyUser.objects.get(email = email)
                print(userdata.password)
                if userdata.check_password(password):
                    user.set_password(newpassword)
                    user.save()
                    return Response("Password Reset successfullyy !!")
                else:
                    return Response("You've entered wrong Password...!!")
                
        except Exception as e :
            return Response(str(e))

import random    
import time

global_otp = 0
class Forgetpassword(APIView):
    def post(self, request):
        givenemail = request.data["email"]
        
        try:
            user = MyUser.objects.get(email = givenemail)
            
        except MyUser.DoesNotExist:
            return Response("Create your account first !!")
        
        if givenemail is None:
            return Response("Email is required !!!")
        
        global global_otp
        global_otp = random.randint(1000, 9999)
        
        emailsend = EmailMessage(
            "Forget Password subject",
            f"your otp is : {global_otp}",
            settings.EMAIL_HOST_USER,
            [givenemail]
        )
        emailsend.send(fail_silently = False)
        return Response({"status" : True, "message" : "email send succesfully !"})
        
globalvarification = False

class varify_password(APIView):
    def post(self, request):
        givendata = request.data 
        email = request.data["email"]
        given_otp = int(request.data["otp"])
        
        try:
            user = MyUser.objects.get(email = email)
            
        except MyUser.DoesNotExist:
            return Response("Create your account first !!")
        
        if given_otp == global_otp:
            global globalvarification
            globalvarification = True
            return Response("Email verified successfully !!")
        else:
            return Response("Invalid OTP !!")
        

class NewPassword(APIView):
    def post(self , reqeust):
        email = reqeust.data["email"]
        NewPassword = reqeust.data["NewPassword"]
        
        try:
            user = MyUser.objects.get(email = email)
            
        except MyUser.DoesNotExist:
            return Response("Create your account first !!")
        if globalvarification == True:
            if email is not None:
                user.set_password(NewPassword)
                user.save()
                return Response("your Password updated successfulyy !!")
        else:
            return Response("Hit Reset API first...!")
        
            