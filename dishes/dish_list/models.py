from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DishList(models.Model):
    dish=models.CharField(max_length=100)
    meal_type=models.CharField(max_length=100)
    time_to_prepare=models.IntegerField()
    cuisine=models.CharField(max_length=100)
    main_ingredient=models.CharField(max_length=100)
    img=models.ImageField(upload_to="food_pics",null=True)

class Review(models.Model):
    review=models.CharField(max_length=500)
    rating=models.FloatField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dish=models.ForeignKey(DishList,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
