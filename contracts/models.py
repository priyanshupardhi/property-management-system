
from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from members.models import Member
from properties.models import Unit


class Contract(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="contracts")
    unit = models.ForeignKey( Unit, on_delete=models.PROTECT, related_name="contracts")

    start_date = models.DateField()
    end_date = models.DateField()

    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)

    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00") )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError({
                "end_date": "End date must be on or after start date."
            })

        if self.monthly_rent <= 0:
            raise ValidationError({
                "monthly_rent": "Monthly rent must be greater than zero."
            })
            
    def calculate_contract_value(self):
        if not self.start_date or not self.end_date or self.monthly_rent is None:
            return Decimal("0.00")

        if self.end_date < self.start_date:
            return Decimal("0.00")

        total = Decimal("0.00")
        current_date = self.start_date

        while current_date <= self.end_date:
            next_month = current_date + relativedelta(months=1)
            period_end = next_month - timedelta(days=1)

            end_date = min(self.end_date, period_end)
            days = (end_date - current_date).days + 1
            total_days = (period_end - current_date).days + 1

            total += self.monthly_rent * Decimal(days) / Decimal(total_days)
            current_date = next_month

        return total.quantize(Decimal("0.01"))

    def save(self, *args, **kwargs):
        self.full_clean()
        self.total_value = self.calculate_contract_value()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.member.full_name} - {self.unit}"
