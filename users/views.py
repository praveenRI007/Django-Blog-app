from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
import asyncio
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm , LoginForm , ProfileUpdateForm , UserUpdateForms , MyChangeFormPassword
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from django.http import HttpResponse
from django.contrib.auth import get_user_model


import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
from .auth import *
# Create your views here.


# @api_view(['POST'])
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"your account is now created , now you are able to login for {username}")
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form': form})

# @api_view(['GET'])
def user(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return Response({'user': serialized_user })


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
@ensure_csrf_cookie
def login_get(request):
    return render(request, 'users/login.html')


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
@ensure_csrf_cookie
def login_post(request):
    User = get_user_model()
    form = LoginForm(request.POST)
    username = request.POST["username"]
    password = request.POST["password"]
    # username = request.data.get('username')
    # password = request.data.get('password')

    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    user = User.objects.filter(username=username).first()

    if(user is None):
        messages.success(request, f"user not found")
        return redirect('login')
        #raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        messages.success(request, f"password incorrect")
        return redirect('login')
        #raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = UserSerializer(user).data

    access_token , exp = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response = redirect('blog-home')
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    response.set_cookie(key='access_token_expiry',value=exp,httponly=False)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }
    return response

@api_view(['GET','POST'])
@permission_classes([AllowAny])
@login_required()
def profile(request):
    if request.POST:
        u_form = UserUpdateForms(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'your account have been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForms(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'users/profile.html',context)

@api_view(['POST','GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def refresh_token(request):
    response = Response({"redirect": "/blog"})
    try:
        refresh_token = request.COOKIES.get('refreshtoken')
        payload_rt = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return render(request, 'users/login.html')

    User = get_user_model()
    user = User.objects.filter(id=payload_rt['user_id']).first()

    if user is None:
        return render(request, 'users/login.html')
        # raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        return render(request, 'users/login.html')
        # raise exceptions.AuthenticationFailed('user is inactive')
    messages.success(request, f" access token expired , new token created using refresh token")
    new_access_token, exp = generate_access_token(user)
    response.set_cookie(key='access_token', value=new_access_token, httponly=True)
    response.set_cookie(key='access_token_expiry',value=exp,httponly=False)
    return response

@api_view(['GET','POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def logout(request):
    response = render(request,'users/logout.html')
    response.delete_cookie('access_token')
    response.delete_cookie('access_token_expiry')
    response.delete_cookie('refreshtoken')
    return response


@api_view(['GET', 'POST'])
@login_required()
def resetpassword(request):
    if request.method == 'POST':
        form_edit_password = MyChangeFormPassword(user=request.user,data=request.POST)
        if form_edit_password.is_valid():
            form_edit_password.save()
            messages.success(request,'Password updated')
            return redirect('blog-home')
        else:
            messages.success(request, 'some error occured while changing password , please check if passwords match and if you have entered correct old password')
            return redirect('blog-home')
    else:
        return render(request, 'users/resetpassword.html')



