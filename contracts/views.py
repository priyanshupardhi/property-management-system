
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Contract
from .serializers import ContractSerializer


class ContractListCreateView(generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Contract.objects.select_related("member", "unit", "unit__property").order_by("-created_at")

        active = self.request.query_params.get("active")

        if active is not None:
            if active.lower() not in ("true", "false"):
                raise ValidationError({
                    "active": "Use true or false."
                })

            if active.lower() == "true":
                today = timezone.localdate()
                queryset = queryset.filter(
                    start_date__lte=today,
                    end_date__gte=today,
                )

        return queryset

    @transaction.atomic
    def perform_create(self, serializer):
        unit = serializer.validated_data["unit"]
        start_date = serializer.validated_data["start_date"]
        end_date = serializer.validated_data["end_date"]

        # Lock the unit row while checking and creating a contract.
        from properties.models import Unit

        unit = Unit.objects.select_for_update().get(pk=unit.pk)

        overlaps = Contract.objects.filter(
            unit=unit,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exists()

        if overlaps:
            raise ValidationError({
                "unit": "This unit already has a contract for overlapping dates."
            })

        contract = serializer.save(unit=unit)

        today = timezone.localdate()
        if contract.start_date <= today <= contract.end_date:
            unit.status = Unit.Status.OCCUPIED
            unit.save(update_fields=["status"])
