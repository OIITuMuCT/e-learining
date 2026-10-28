from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # 1. ОБЯЗАТЕЛЬНО проверьте, что 'username' есть в этом списке!
        fields = ['username', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        # Удаляем проверочный пароль, он не нужен модели User
        validated_data.pop('password_confirm', None)

        # 2. Безопасное извлечение данных (для надежности передаем явно)
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        if not username:
            raise serializers.ValidationError({"username": "Это поле обязательно для создания пользователя."})

        # Создаем пользователя через менеджер
        user = User.objects.create_user(
            username=username,
            password=password,
            **validated_data  # передаем остальные поля, если они есть (например, email, first_name)
        )
        return user
