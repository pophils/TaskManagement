

from django.conf.urls import patterns, url
from .controller.authentication_view import signin, signout

urlpatterns = patterns('',
                       url(r'^login/', signin, name='login'),
                       url(r'^logout/', signout, name='logout'),
                       )
