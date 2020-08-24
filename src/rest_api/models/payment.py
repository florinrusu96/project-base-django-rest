from django.db import models


class Payment(models.Model):
    # we don't save the credit_card_number or security code, usually the payment service deals with those,
    # we just want a history
    card_holder = models.CharField(max_length=256)
    expiration_date = models.DateField()
    amount = models.PositiveIntegerField()
