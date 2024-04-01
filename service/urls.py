from django.urls import path
from service.views import (ListCreateCollectAPIView,
                           CollectAPIView)


urlpatterns = [
    # path('user/reg/', RegistrationView.as_view(), name='reg'),
    # path('user/change-passwd', ChangePasswordView.as_view(),
    #      name='change_passwd'),
    # path('user/profile/', MeView.as_view(), name='profile'),
    path('collects/', ListCreateCollectAPIView.as_view(), name='collects'),
    path('collects/<int:pk>/', CollectAPIView.as_view(), name='collect'),
]
