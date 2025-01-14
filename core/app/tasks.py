from celery import shared_task
from django.conf import settings
import redis
import time


r_client = redis.StrictRedis.from_url(settings.REDIS_URL)


@shared_task
def add(x, y):
    count = 0
    while count < 5:
        print(f"add {count}", x, y)
        time.sleep(2)
        count += 1
    return x + y


@shared_task(name='mul')
def mul(x, y):
    return x * y


@shared_task(name="monitor_redis")
def monitor_redis():

    from .helpers import get_deployment_names, create_worker_for_user, delete_worker_for_user
    deployment_names = get_deployment_names()
    print('monitoring redis...')
    queues = r_client.keys('celery-worker-*')
    print("queues", queues)
    for queue in queues:
        queue_name = queue.decode()
        key_type = r_client.type(queue_name).decode('utf-8')

        if key_type == 'list':
            length = r_client.llen(queue_name)
            print(f"List '{queue_name}' has {length} items.")

        else:
            print(f"Key '{queue_name}' is of type '{key_type}', skipping.")

        if length > 0 and queue_name not in deployment_names:
            username = queue_name.split('worker-')[1]
            create_worker_for_user(username)


@shared_task(name="terminate_worker")
def terminate_worker():
    print("terminate_worker")
    from core.celery import app
    inspect = app.control.inspect()

    from .helpers import get_deployment_names, delete_worker_for_user
    deployment_names = get_deployment_names()
    print("deployment_names", deployment_names)

    active_queues = inspect.active()
    reserved_queues = inspect.reserved()
    scheduled_queues = inspect.scheduled()

    print("active_queues", active_queues, "reserved_queues", reserved_queues, "scheduled_queues", scheduled_queues)

    for k in active_queues.keys():
        if not active_queues[k] and not reserved_queues[k]\
             and not scheduled_queues[k]:
            import re
            s = k
            match = re.search(r'@([\w-]+)-\d', s)
            if match:
                result = match.group(1)
                print("result", result)  # Output: celery-worker-test
                if result in deployment_names:
                    delete_worker_for_user(result)

    # username = queue_name.split('worker-')[1]
    # delete_worker_for_user(username)
