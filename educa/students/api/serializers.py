from django.contrib.auth import  get_user_model
from rest_framework import serializers

User = get_user_model()

class StudentRegistrationSerializer(serializers.Serializer):
    # Явно указываем поля для паролей. `write_only=True` означает,
    # что пароль можно прислать в POST-запросе, но в ответе API его не будет
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        # Метод create_user гарантированно есть у любого стандартного или правильно расширенного менеджера пользователей
        return User.objects.create_user(**validated_data)