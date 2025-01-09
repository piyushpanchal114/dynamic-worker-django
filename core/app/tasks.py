from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task(name='mul')
def mul(x, y):
    return x * y
