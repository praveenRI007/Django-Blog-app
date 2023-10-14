from django.urls import include, path
from .views import user,login_get , login_post , profile , refresh_token , logout , resetpassword
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login_get', login_get, name='login'),
    path('login_post', login_post, name='login_post'),
    path('user', user, name='user'),
    path('profile',profile,name='profile'),
    path('refresh_token',refresh_token,name='refresh_token'),
    path('logout',logout,name='logout'),
    path('reset-password',resetpassword,name='reset-password'),

]