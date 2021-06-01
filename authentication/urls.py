from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("ip-config/", views.api_ip),
    path("login/", views.login_view),
    path("logout/", views.logout_view)
]