from django.contrib.auth.password_validation import validate_password
from service.models import Collect, Reason, Payment, User
from rest_framework.exceptions import ParseError
from rest_framework import serializers


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('name',)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'collect',
            'amount',
            'user',
            'payment_date',
        )
        read_only_fields = ('payment_date', 'user')


class CollectSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True)

    class Meta:
        model = Collect
        fields = (
            'id',
            'author',
            'title',
            'reason',
            'description',
            'goal',
            'current_amount',
            'users_count',
            'image',
            'deadline',
            'payments',
        )
        read_only_fields = ('author', 'current_amount', 'users_count',)


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                'Пользователь с такой почтой уже зарегистрирован.'
            )
        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
