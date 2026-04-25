from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User
from accounts.permissions import check_permissions
from accounts.serializers import RegistrationSerializer
from accounts.serializers import LoginSerializer
from accounts.utils import generate_jwt_token
from accounts.models import BlacklistedToken


class RegisterView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Пользователь создан"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            token = generate_jwt_token(user)

            return Response(
                {
                    "message": "Успешный вход",
                    "token": token
                }
            )

        return Response(
            serializer.errors,
            status=400
        )


from rest_framework.views import APIView
from rest_framework.response import Response


class TestView(APIView):

    def get(self, request):
        if not request.custom_user or not isinstance(request.custom_user, User):
            return Response({
                "error": "Нет пользователя"
            }, status=401)

        return Response({
            "user": request.custom_user.email
        })


class OrdersView(APIView):

    def get(self, request):
        if not request.custom_user or not isinstance(request.custom_user, User):
            return Response({"error": "Не авторизован"}, status=401)

        if not check_permissions(request.custom_user, "orders", "read"):
            return Response({"error": "Доступ запрещён"}, status=403)

        return Response({"data": "Список заказов"})


class LogoutView(APIView):

    def post(self, request):

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Нет токена"}, status=400)

        try:
            prefix, token = auth_header.split()

            if prefix != "Bearer":
                return Response({"error": "Неверный формат токена"}, status=400)

            BlacklistedToken.objects.create(token=token)

            return Response({"message": "Вы вышли из системы"})

        except Exception as e:
            return Response({"error": str(e)}, status=400)