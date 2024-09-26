import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
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
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            request.user = None  # Assign None if no token is found

        return self.get_response(request)

class JWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            request.user = AnonymousUser()  # No token, set user as Anonymous
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            request.user = user
            request.user.role = payload['role']  # Add role to request user
        except jwt.ExpiredSignatureError:
            request.user = AnonymousUser()  # Token expired, anonymous user
        except jwt.InvalidTokenError:
            request.user = AnonymousUser()  # Invalid token, anonymous user

        return None
