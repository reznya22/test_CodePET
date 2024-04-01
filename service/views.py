from rest_framework import generics
from service.models import Collect
from service.permissions import IsAuthorOrStaff
from service.serializers import CollectSerializer


class ListCreateCollectAPIView(generics.ListCreateAPIView):
    """Get all collects"""
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [IsAuthorOrStaff,]


class CollectAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Get/delete/update one collect"""
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [IsAuthorOrStaff, ]
