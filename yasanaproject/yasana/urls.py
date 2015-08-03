

from django.conf.urls import url, patterns
from .controller.landing import LandingView

urlpatterns = patterns('',
                       url(r'^$', LandingView.as_view(), name='landing'),
                       )
