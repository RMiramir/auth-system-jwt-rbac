import bcrypt
from rest_framework import serializers
from accounts.models import User

class RegistrationSerializer(serializers.Serializer):
    # ПОЛЯ, КОТОРЫЕ ПРИХОДЯТ ОТ ПОЛЬЗОВАТЕЛЯ
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)

    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    # Валидация
    def validate(self, data):
        # Здесь мы проверяем данные.
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Пароли не совпадают')

        return data

    # Создание пользователя
    def create(self, validated_data):

        validated_data.pop('password_confirm')
        raw_password = validated_data.pop('password')

        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User.objects.create(password_hash=hashed_password, **validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")


        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")


        if not user.is_active:
            raise serializers.ValidationError("Аккаунт деактивирован")


        password_valid = bcrypt.checkpw(
            password.encode('utf-8'),
            user.password_hash.encode('utf-8')
        )

        if not password_valid:
            raise serializers.ValidationError("Неверный пароль")

        data["user"] = user
        return data



