

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class LandingView(TemplateView):
    template_name = 'yasana/landing.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(reverse('account:login'))

        return super(LandingView, self).get(request, *args, **kwargs)
