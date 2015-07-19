

from celery import Celery


task_cloud = Celery('django_task', broker='amqp://guest:putamadre@localhost:5672//')


@task_cloud.task
def print_square(num):
    print('The square of {} is {}'.format(num, num * num))


@task_cloud.task
def print_name_twice(name):
    print(name * 2)
