from django.conf.urls import url
from rest_api import views

urlpatterns = [url(r"payment/", views.PaymentCreate.as_view(), name="payment"),
               url(r"prediction/", views.PriceEstimationView.as_view(), name="price-estimation"), ]
