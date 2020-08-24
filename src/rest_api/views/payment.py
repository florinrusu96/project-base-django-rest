from rest_framework import generics, status
from rest_framework.response import Response

from rest_api import external_service
from rest_api import serializers, models


class PaymentCreate(generics.CreateAPIView):
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        amount = validated_data.get('amount')
        if amount <= 20:
            self._process_cheap_payment(validated_data)
        elif amount < 500:
            self._process_expensive_payment(validated_data)
        else:
            self._process_premium_payment(validated_data)

        self.perform_create(validated_data)

        return Response(serializer.data)

    def perform_create(self, validated_data):
        models.Payment.objects.create(
            card_holder=validated_data.get("card_holder"),
            expiration_date=validated_data.get("expiration_date"),
            amount=validated_data.get("amount"),
        )

    def _process_premium_payment(self, validated_data, retries=0):
        try:
            external_service.PremiumPaymentGateway()
        except Exception:
            if retries <= 3:
                self._process_premium_payment(validated_data, retries=retries + 1)
            raise Exception("Internal server error")
        else:
            pass

    def _process_expensive_payment(self, validated_data):
        try:
            external_service.ExpensivePaymentGateway()
        except Exception:
            self._process_cheap_payment(validated_data)
        else:
            pass

    @staticmethod
    def _process_cheap_payment(validated_data):
        external_service.CheapPaymentGateway()
