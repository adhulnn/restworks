from django.shortcuts import render
from .models import movies,MovieList,Review
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet,ModelViewSet
from .serializer import MovieSerializer,MovieModelSer,UserSerializer,ReviewSerializer
from rest_framework import status
from rest_framework import permissions,authentication
from rest_framework.decorators import action


# Create your views here.
class MovieLst(APIView):
    def get(self,request,*args,**kwargs):
        mvs=MovieList.objects.all()
        ser=MovieSerializer(mvs,many=True)
        return Response(data=ser.data)
    def post(self,request,*args,**kwargs):
        mv=request.data
        ser=MovieSerializer(data=mv)
        if ser.is_valid():
            name=ser.validated_data.get("name")
            year=ser.validated_data.get("year")
            director=ser.validated_data.get("director")
            genre=ser.validated_data.get("genre")
            MovieList.objects.create(name=name,year=year,director=director,genre=genre)
            return Response({"msg":"ok"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_417_EXPECTATION_FAILED)
class MovieItem(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('mid')
        mvs=MovieList.objects.get(id=id)
        ser=MovieSerializer(mvs)
        return Response(data=ser.data)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get('mid')
        mvs=MovieList.objects.get(id=id)
        mvs.delete()
        return Response({"msg":"deleted"})
    def put(self,request,*args,**kwargs):
        id=kwargs.get('mid')
        mvs=MovieList.objects.get(id=id)
        moviedata=request.data
        ser=MovieSerializer(data=moviedata)
        if ser.is_valid():
            mvs.name=ser.validated_data.get("name")
            mvs.year=ser.validated_data.get("year")
            mvs.director=ser.validated_data.get("director")
            mvs.genre=ser.validated_data.get("genre")
            mvs.save()
            return Response({"msg":"updated"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_404_NOT_FOUND)

class MovieModelList(APIView):
    def get(self,request,*args,**kwargs):
        mvs=MovieList.objects.all()
        dser=MovieModelSer(mvs,many=True)
        return Response(data=dser.data)
    def post(self,request,*args,**kwargs):
        mvs=request.data
        ser=MovieModelSer(data=mvs)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"created"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_404_NOT_FOUND)
class MovieModelItem(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("mid")
        try:
            mv=MovieList.objects.get(id=id)
            dser=MovieModelSer(mv)
            return Response(dser.data)
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("mid")
        try:
            mv=MovieList.objects.get(id=id)
            mv.delete()
            return Response({"msg":"deleted"})
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("mid")
        try:
            mv=MovieList.objects.get(id=id)
            ser=MovieModelSer(data=request.data,instance=mv)
            if ser.is_valid():
                ser.save()
                return Response({"msg":"updated"})
            else:
                return Response({"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_400_BAD_REQUEST)

class UserCreationView(APIView):
    def post(self,request,*args,**kwargs):
        ser=UserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"registration completed"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class MovieApi(ViewSet):
    def list(self,request,*args,**kwargs):
        mvs=MovieList.objects.all()
        dser=MovieModelSer(mvs,many=True)
        return Response(data=dser.data)
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            mv=MovieList.objects.get(id=id)
            dser=MovieModelSer(mv)
            return Response(dser.data)
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_400_BAD_REQUEST)
    def create(self,request,*args,**kwargs):
        mvs=request.data
        ser=MovieModelSer(data=mvs)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"created"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_404_NOT_FOUND)
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            mv=MovieList.objects.get(id=id)
            ser=MovieModelSer(data=request.data,instance=mv)
            if ser.is_valid():
                ser.save()
                return Response({"msg":"updated"})
            else:
                return Response({"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_400_BAD_REQUEST)
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            MovieList.objects.filter(id=id).delete()
            return Response({"msg":"deleted"})
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_400_BAD_REQUEST)

# using modelviewset
#mvapi/2/add_reviews

class MovieApiMV(ModelViewSet):
    serializer_class=MovieModelSer
    queryset=MovieList.objects.all()
    model=MovieList
    permission_classes=[permissions.IsAuthenticated]
    # authentication_classes=[authentication.TokenAuthentication]

    @action(detail=True, methods=['post'])
    def add_reviews(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mv=MovieList.objects.get(id=id)
        user=request.user
        ser=ReviewSerializer(data=request.data,context={"user":user,"movie":mv})
        if ser.is_valid():
            ser.save()
            return Response({"msg":"ADDED"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'])
    def get_reviews(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            mv=MovieList.objects.get(id=id)
            review=Review.objects.filter(movie=mv)
            dser=ReviewSerializer(review,many=True)
            return Response(dser.data)
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_400_BAD_REQUEST)
    