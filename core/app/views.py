import os
import redis
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .tasks import add


r_client = redis.Redis(host=os.environ['REDIS_HOSTNAME'],
                       port=os.environ['REDIS_PORT'],
                       password=os.environ['REDIS_PASSWORD'], db=2)


@api_view(['GET'])
def redis_keys(request):
    print("redis", r_client.keys())
    return Response({"data": r_client.keys()})


@api_view(['GET'])
def call_add_task(request):
    id = add.delay(1, 2)
    print("id", id)
    return Response({"data": "id"})
