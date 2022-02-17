from ast import If
from urllib import response
from django.shortcuts import render
import json
# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.permissions import IsAuthenticated


from knox.auth import TokenAuthentication   
from Myapp.models import JsonData
from .serializers import UserSerializer, RegisterSerializer,JsonUploadSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
        
        
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
    

class ParseInputDataView(APIView):
  
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # def dispatch(self,request,*args,**kwargs):
    #     print(request.meta)
        # return super().dispatch(request,*args,**kwargs)
    def post(self, request,  format=None):
        print(request.FILES)
       
        file_entry =  request.FILES.getlist('file')[0]
        # uploaded_file_name = file_entry.name
        uploaded_file_content = file_entry.read()
        try:
            
            uploaded_file_content = json.loads(uploaded_file_content)
            serializer = JsonUploadSerializer(data={"json_data":uploaded_file_content, 'user':request.user.id})
          
            
            if serializer.is_valid():
                json_data = serializer.save()
                    
                return Response(status=201,data=JsonUploadSerializer(instance = json_data).data)
                
            else:
                return Response(status=400,data=serializer.error_messages)
        except Exception as e:
             return Response(status=400,data={"error":str(e)})