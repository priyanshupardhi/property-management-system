
from rest_framework import serializers

from .models import Property, Unit


class UnitSerializer(serializers.ModelSerializer):
    property_id = serializers.IntegerField(
        source="property.id",
        read_only=True,
    )

    class Meta:
        model = Unit
        fields = [
            "id",
            "property_id",
            "unit_number",
            "monthly_rent",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "property_id",
            "created_at",
            "updated_at",
        ]

    def validate_monthly_rent(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Monthly rent cannot be negative."
            )
        return value


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            "id",
            "name",
            "address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PropertyDetailSerializer(PropertySerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta(PropertySerializer.Meta):
        fields = PropertySerializer.Meta.fields + ["units"]
