from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('jwt')

        if token:
            try:
                # Decode the JWT token
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                # Retrieve the user from the database
                user = User.objects.get(id=payload['user_id'])
                # Attach the user and role to the request
                request.user = user
                request.role = payload.get('role', None)  # Attach the role to the request
            except jwt.ExpiredSignatureError:
                return redirect('login')  # Redirect to login if token is expired
            except jwt.DecodeError:
                return redirect('login')  # Redirect to login if token is invalid
            except User.DoesNotExist:
                request.user = AnonymousUser()  # Set user as AnonymousUser if not found
                request.role = None
        else:
            request.user = AnonymousUser()  # No token present, set user as AnonymousUser
            request.role = None
