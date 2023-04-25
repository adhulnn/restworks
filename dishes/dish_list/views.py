from django.shortcuts import render
from .models import DishList,Review
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from .serializer import UserSerializer,DishModelSer
from rest_framework import status
from rest_framework import permissions,authentication
from rest_framework.decorators  import action
# Create your views here.

class UserCreationView(APIView):
    def post(self,request,*args,**kwargs):
        ser=UserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"registration completed"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class DishApiMV(ModelViewSet):
    serializer_class=DishModelSer
    queryset=DishList.objects.all()
    model=DishList
    permission_classes=[permissions.IsAuthenticated]

