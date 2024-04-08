from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from collect_service.services import get_collects_cache
from service.permissions import IsAuthorOrStaff
from django.contrib.auth import get_user_model
from service.tasks import send_to_email
from rest_framework import generics
from service.models import Collect
from service.serializers import *
from django.db.models import F

User = get_user_model()


@extend_schema_view(
    get=extend_schema(summary='Список сборов', tags=['Сборы']),
    post=extend_schema(summary='Создание сбора', tags=['Сборы'])
)
class ListCreateCollectAPIView(generics.ListCreateAPIView):
    """Get all collects"""
    serializer_class = CollectSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = get_collects_cache()
        return queryset

    def create(self, request, *args, **kwargs):
        self.kwargs['author'] = self.request.user
        if self.request.user.email:
            username = self.request.user.username
            send_to_email.delay(message=f'Hi {username}, your collect is successful created',
                                recipient_list=self.request.user.email)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.kwargs.get('user'))


@extend_schema_view(
    get=extend_schema(summary='Получить сбор', tags=['Сборы']),
    patch=extend_schema(summary='Обновление сбора', tags=['Сборы']),
    put=extend_schema(summary='Обновление сбора', tags=['Сборы']),
    delete=extend_schema(summary='Удаление сбора', tags=['Сборы'])
)
class CollectAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Get/delete/update one collect"""
    serializer_class = CollectSerializer
    permission_classes = [IsAuthorOrStaff,]

    def get_queryset(self):
        # redis-cache
        return get_collects_cache()


@extend_schema_view(
    post=extend_schema(summary='Создание платежа', tags=['Платежи']))
class PaymentCreateAPIView(generics.CreateAPIView):
    """Create a payment"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated,]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        self.kwargs['user'] = user
        payment_in_collect = Collect.objects.filter(
                                            payments__user=user,
                                            id=request.data.get('collect'))
        collect = Collect.objects.filter(id=request.data.get('collect'))
        if not payment_in_collect:
            collect.update(users_count=F('users_count') + 1)

        collect.update(
            current_amount=F('current_amount') + request.data.get('amount'))
        if self.request.user.email:
            username = self.request.user.username
            send_to_email.delay(message=f'Hi {username}, your payment is successful created',
                                recipient_list=self.request.user.email)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.kwargs.get('user'))


@extend_schema_view(
    post=extend_schema(summary='Регистрация пользователя',
                       tags=['Аутентификация & Авторизация']),
)
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
