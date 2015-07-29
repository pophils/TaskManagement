

from django.conf.urls import patterns, url
from .controller.account import api_get_users, get_users_total_count
from.controller.task import task_summary

urlpatterns = patterns('',
                       url(r'^users/', api_get_users, name='api_get_users'),
                       url(r'^new-user/', api_get_users, name='api_get_users1'),
                       url(r'^task-summary/', task_summary, name='task_summary_on_landing'),
                       url(r'^total-users/', get_users_total_count, name='total_users'),
                       )
