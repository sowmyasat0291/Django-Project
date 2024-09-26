import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User

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
