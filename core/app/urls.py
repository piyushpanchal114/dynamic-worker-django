from . import views
from django.urls import path

urlpatterns = [
    path("r-keys", views.redis_keys),
    path("add-task", views.call_add_task),
]
