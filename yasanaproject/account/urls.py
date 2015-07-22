

from django.conf.urls import patterns, url
from .controller.authentication_view import signin, signout, selenium_login_helper

urlpatterns = patterns('',
                       url(r'^login/', signin, name='login'),
                       url(r'^logout/', signout, name='logout'),
                       url(r'^selenium-login/', selenium_login_helper, name='selenium_login_helper')
                       )
