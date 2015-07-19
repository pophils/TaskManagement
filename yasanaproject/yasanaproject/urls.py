from django.conf.urls import patterns, include, url

from yasana import urls as yasana_urls
from account import urls as account_urls

urlpatterns = patterns('',
                       url(r'^', include(yasana_urls, namespace='yasana')),
                       url(r'^account/', include(account_urls, namespace='account')),
)
