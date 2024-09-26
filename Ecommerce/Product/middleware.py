import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser, User

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt')

        if token:
            try:
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                request.user = User.objects.get(id=decoded['user_id'])  # Attach user to the request
                request.user.role = decoded.get('role')  # Add role to request user if exists
            except jwt.ExpiredSignatureError:
                request.user = AnonymousUser()  # Token expired, anonymous user
            except jwt.InvalidTokenError:
                request.user = AnonymousUser()  # Invalid token, anonymous user
            except User.DoesNotExist:
                request.user = AnonymousUser()  # User does not exist
        else:
            request.user = AnonymousUser()  # No token, set user as Anonymous

        return self.get_response(request)
