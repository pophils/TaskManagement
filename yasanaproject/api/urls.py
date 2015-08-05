

from django.conf.urls import patterns, url
from .controller.account import api_get_users, get_users_total_count
from.controller.task import task_summary, get_task_total_count, api_get_tasks, api_complete_task

urlpatterns = patterns('',
                       url(r'^users/', api_get_users, name='api_get_users'),
                       url(r'^new-user/', api_get_users, name='api_get_users1'),
                       url(r'^task-summary/', task_summary, name='task_summary_on_landing'),
                       url(r'^total-users/', get_users_total_count, name='total_users'),
                       url(r'^total-tasks/', get_task_total_count, name='total_tasks'),
                       url(r'^tasks/', api_get_tasks, name='api_get_tasks'),
                       url(r'^complete-task/', api_complete_task, name='api_complete_task'),
                       # url(r'^update-user/', update_user, name='update_user'),
                       )
