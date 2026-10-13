
from rest_framework import serializers

from .models import Contract
from members.models import Member
from properties.models import Unit


class ContractSerializer(serializers.ModelSerializer):
    total_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Contract
        fields = [
            "id",
            "member",
            "unit",
            "start_date",
            "end_date",
            "monthly_rent",
            "total_value",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "total_value",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "end_date": "End date must be on or after Start date."
            })

        return attrs

    def create(self, validated_data):
        unit = validated_data["unit"]

        if validated_data.get("monthly_rent") is None:
            validated_data["monthly_rent"] = unit.monthly_rent

        return Contract.objects.create(**validated_data)
