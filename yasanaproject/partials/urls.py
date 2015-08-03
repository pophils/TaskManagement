

from django.conf.urls import patterns, url
from .controller.user_management import user_collection_partial, add_user_partial, add_task_partial
from .controller.task_management import task_collection_partial

urlpatterns = patterns('',
                       url(r'^user-collection/', user_collection_partial, name='user_collection_partial'),
                       url(r'^add-user/', add_user_partial, name='add_user_partial'),
                       url(r'^task-collection/', task_collection_partial, name='task_collection_partial'),
                       url(r'^add-task/', add_task_partial, name='add_task_partial'),
                       )
