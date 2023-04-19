"""
URL configuration for movies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import MovieLst,MovieItem,MovieModelList,MovieModelItem,UserCreationView,MovieApi,MovieApiMV
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router=DefaultRouter()
router.register('movieapi',MovieApi,basename="mapi")
router.register('mvapi',MovieApiMV,basename='mvapi')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/',MovieLst.as_view()),
    path('mv/',MovieModelList.as_view()),
    path('movies/<int:mid>',MovieItem.as_view()),
    path('mv/<int:mid>',MovieModelItem.as_view()),
    path('user',UserCreationView.as_view()),
    path('tauth/', views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+router.urls