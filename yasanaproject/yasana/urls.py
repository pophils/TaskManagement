

from django.conf.urls import url, patterns
from .controller.landing import LandingView, landing_task_summary
from .controller.about import AboutView

urlpatterns = patterns('',
                       url(r'^$', LandingView.as_view(), name='landing'),
                       url(r'^about/$', AboutView.as_view(), name='about'),
                       url(r'^landing-task-summary/$', landing_task_summary, name='landing_task_summary')
                       )
