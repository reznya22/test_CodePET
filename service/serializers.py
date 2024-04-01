from rest_framework import serializers
from service.models import Collect, Reason, Payment, User


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
            'amount',
            'user',
            'payment_date',
        )


class CollectSerializer(serializers.ModelSerializer):
    reason = ReasonSerializer()
    author = AuthorSerializer()
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
