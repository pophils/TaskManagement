

from django.conf.urls import url, patterns
from .controller.landing import LandingView, landing_task_summary

urlpatterns = patterns('',
                       url(r'^$', LandingView.as_view(), name='landing'),
                       )
