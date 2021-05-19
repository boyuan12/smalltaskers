from django.urls import path
from . import views

urlpatterns = [
    path("deposit/", views.accept_payment_view),
    path("payment-success/", views.payment_success)
]