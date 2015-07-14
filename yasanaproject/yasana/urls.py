

from django.conf.urls import url, patterns

urlpatterns = patterns('',
                       url(r'^$', name='landing'),
                       url(r'^about/$')
                       )
