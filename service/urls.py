from django.urls import path
from service.views import (ListCreateCollectAPIView,
                           CollectAPIView,
                           PaymentCreateAPIView,
                           RegistrationView)


urlpatterns = [
    path('user/reg/', RegistrationView.as_view(), name='reg'),
    path('collects/', ListCreateCollectAPIView.as_view(), name='collects'),
    path('collects/<int:pk>/', CollectAPIView.as_view(), name='collect'),
    path('payment-create/', PaymentCreateAPIView.as_view(), name='payment'),
]
