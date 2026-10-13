from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Property, Unit
from .serializers import (
    PropertySerializer,
    PropertyDetailSerializer,
    UnitSerializer,
)


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all().order_by("-created_at")
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]


class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.prefetch_related("units")
    serializer_class = PropertyDetailSerializer
    permission_classes = [IsAuthenticated]


class UnitListView(generics.ListAPIView):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Unit.objects.select_related("property").order_by("id")
        status_value = self.request.query_params.get("status")

        if status_value is not None:
            valid_statuses = Unit.Status.values

            if status_value not in valid_statuses:
                raise ValidationError({
                    "status": [
                        f"Invalid status. Choose from: {', '.join(valid_statuses)}."
                    ]
                })

            queryset = queryset.filter(status=status_value)

        return queryset


class UnitCreateView(generics.CreateAPIView):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property_obj = get_object_or_404(
            Property,
            pk=self.kwargs["property_id"],
        )
        serializer.save(property=property_obj)
