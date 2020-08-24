from datetime import datetime

from rest_framework import serializers

from rest_api import models


class PaymentSerializer(serializers.ModelSerializer):
    credit_card_number = serializers.CharField(max_length=19, write_only=True)
    security_code = serializers.CharField(max_length=3, min_length=3, write_only=True, allow_blank=True,
                                          allow_null=True)

    class Meta:
        model = models.Payment
        fields = ["credit_card_number", "security_code", "card_holder", "amount", "expiration_date"]

    def validate_credit_card_number(self, credit_card_number):
        if len(credit_card_number) < 10:
            raise serializers.ValidationError("Not a valid credit card number")
        return credit_card_number

    def validate_expiration_date(self, date):
        if date < datetime.today().date():
            return serializers.ValidationError("Expiration date not valid")
        return date
