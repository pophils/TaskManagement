

from django.conf.urls import url, patterns
from .controller.landing import LandingView
from .controller.about import AboutView

urlpatterns = patterns('',
                       url(r'^$', LandingView.as_view(), name='landing'),
                       url(r'^about/$', AboutView.as_view(), name='about')
                       )
