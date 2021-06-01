from django.urls import path
from . import views

urlpatterns = [
    path("post-job/", views.post_job)
]