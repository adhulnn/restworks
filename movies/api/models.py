from django.db import models
from django.contrib.auth.models import User

# Create your models here.
movies=[
    {"id":1,"name":"Sphadikam","year":1996,"director":"Bhadran","genre":"drama"},
    {"id":2,"name":"Premam","year":2015,"director":"Alphonse","genre":"romance"},
    {"id":3,"name":"Lucifer","year":2019,"director":"Prithviraj","genre":"drama"},
    {"id":4,"name":"Iron Man","year":2008,"director":"John","genre":"action"},
    {"id":5,"name":"DSMM","year":2022,"director":"Sam Riami","genre":"action"},
]

class MovieList(models.Model):
    name=models.CharField(max_length=100)
    year=models.IntegerField()
    director=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    img=models.ImageField(upload_to="movie_pics",null=True)

class Review(models.Model):
    review=models.CharField(max_length=500)
    rating=models.FloatField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(MovieList,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)