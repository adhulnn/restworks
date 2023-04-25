from rest_framework import serializers
from .models import DishList,Review
from django.contrib.auth.models import User

class DishModelSer(serializers.Serializer):
    class Meta:
        model=DishList
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class DishSer(serializers.ModelSerializer):
    class Meta:
        model=DishList
        fields=["dish","cusine"]

class UserRevSer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","username"]
    

class ReviewSerializer(serializers.ModelSerializer):
    dish=DishSer(read_only=True)
    user=UserRevSer(read_only=True)
    class Meta:
        model=Review
        fields=["review","rating","date","dish","user"]
    def create(self,validated_data):
        user=self.context.get("user")
        mv=self.context.get("movie")
        return Review.objects.create(**validated_data,user=user,movie=mv)