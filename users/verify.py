import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from rest_framework.response import Response
from django.shortcuts import render , redirect

from users.auth import generate_access_token


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        User = get_user_model()
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return None
        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            messages.success(request, f" access token expired")
            return None
            #raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            return None
            #raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(id=payload['user_id']).first()
        if user is None:
            return None
            #raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            return None
            #raise exceptions.AuthenticationFailed('user is inactive')

        self.enforce_csrf(request)

        print('verified')
        return (user, None)

    def enforce_csrf(self, request):
        check = CSRFCheck(get_response=request)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)