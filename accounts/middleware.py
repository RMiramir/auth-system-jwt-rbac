import jwt
from django.conf import settings
from accounts.models import User, BlacklistedToken


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.custom_user = None

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return self.get_response(request)

        try:
            parts = auth_header.split()

            if len(parts) != 2:
                return self.get_response(request)

            prefix, token = parts

            if prefix != "Bearer":
                return self.get_response(request)

            if BlacklistedToken.objects.filter(token=token).exists():
                print("Токен в blacklist (logout)")
                return self.get_response(request)

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            user_id = payload.get("user_id")

            if not user_id:
                return self.get_response(request)

            user = User.objects.get(id=user_id)

            request.custom_user = user

        except jwt.ExpiredSignatureError:
            print("Токен истёк")

        except jwt.InvalidTokenError:
            print("Неверный токен")

        except User.DoesNotExist:
            print("Пользователь не найден")

        return self.get_response(request)