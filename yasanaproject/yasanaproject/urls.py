from django.conf.urls import patterns, include, url
from django.contrib import admin

from yasana import urls as yasana_url

urlpatterns = patterns('',
                       url(r'^', include(yasana_url, namespace='yasana')),
    # Examples:
    # url(r'^$', 'yasanaproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)
