from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("post-job/", views.post_job),
    path("task/<int:task_id>/", views.view_task),
    path("api/upload/", views.file_upload_backend),
    path("tasks/", views.jobs_submitted_tasker),
    path("tasker/job/cancel/<int:job_id>", views.cancel_job)
]