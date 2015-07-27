

from django.conf.urls import patterns, url
from .controller.account import api_get_users

urlpatterns = patterns('',
                       url(r'^users/', api_get_users, name='api_get_users'),

                       )
