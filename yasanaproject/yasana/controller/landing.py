

from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse


class LandingView(TemplateView):
    template_name = 'yasana/landing.html'

    def get(self, request, *args, **kwargs):
        print(request.user)
        if not request.user.is_authenticated():
            print(123456)
            return redirect(reverse('account:login'))

        return render(request, self.template_name)




