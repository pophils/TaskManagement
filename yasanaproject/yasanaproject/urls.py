from django.conf.urls import patterns, include, url

from yasana import urls as yasana_urls
from account import urls as account_urls
from api import urls as api_urls
from partials import urls as partial_urls

urlpatterns = patterns('',
                       url(r'^', include(yasana_urls, namespace='yasana')),
                       url(r'^account/', include(account_urls, namespace='account')),
                       url(r'^api/', include(api_urls, namespace='api')),
                       url(r'^partials/', include(partial_urls, namespace='partials')),
                       )
