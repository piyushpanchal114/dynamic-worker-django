import redis
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .tasks import add


r_client = redis.Redis.from_url(settings.REDIS_URL)


@api_view(['GET'])
def redis_keys(request):
    print("redis", r_client.keys())
    from core.celery import app

    inspect = app.control.inspect()
    print("inspect", inspect.active())
    print("inspect", inspect.scheduled())
    print("inspect", inspect.reserved())
    return Response({"data": r_client.keys()})


@api_view(['GET'])
def call_add_task(request):
    # id = add.delay(1, 2)
    id = add.apply_async((2, 2), queue='lopri')
    print("id", id)
    return Response({"data": "id"})


from rest_framework.views import APIView
from django.contrib.auth.models import User
from .helpers import create_worker_for_user, create_worker_job


class SpinWorker(APIView):

    def get(self, request):
        q = self.request.query_params.get('q')
        print("q", q)
        user = User.objects.get(username=q)
        create_worker_for_user(user.username)
        return Response({"data": "worker created"})


class AddTask(APIView):

    def get(self, request):
        q = self.request.query_params.get('q')
        print("q", q)
        user = User.objects.get(username=q)
        id = add.apply_async((2, 2), queue=f'user_queue_{user.username}')
        print("id", id)
        return Response({"data": "id"})


class SpinJob(APIView):

    def get(self, request):
        q = self.request.query_params.get('q')
        print("q", q)
        user = User.objects.get(username=q)
        create_worker_job(user.username)
        return Response({"data": "worker job created"})
