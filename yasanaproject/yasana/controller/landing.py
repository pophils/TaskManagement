
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as api_status
from django.contrib.auth import get_user_model
from django.db.models import Count
from ..models.user_task import Task


class LandingView(TemplateView):
    template_name = 'yasana/landing.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated():
            return redirect(reverse('account:login'))
        return super(LandingView, self).get(request, *args, **kwargs)
