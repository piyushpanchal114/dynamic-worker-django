from . import views
from django.urls import path

urlpatterns = [
    path("r-keys", views.redis_keys),
    path("add-task", views.call_add_task),
    path("spin-worker", views.SpinWorker.as_view()),
    path("task-add", views.AddTask.as_view()),
    path("spin-job", views.SpinJob.as_view()),
]
