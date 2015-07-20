

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from ..core.forms.login_form import LoginForm


def signin(request):

    if request.method == 'GET':
        if request.user and request.user.is_authenticated() and request.user.is_active:
            return redirect(reverse('yasana:landing'))
        return render(request, 'account/login.html', {'login_form': LoginForm()})
    else:

        if request.user and request.user.is_authenticated() and request.user.is_active:
            return redirect(reverse('yasana:landing'))
        form = LoginForm(data=request.POST)

        if form.is_valid():
            logged_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])

            if logged_user and logged_user.is_active:
                login(request, logged_user)
                return redirect(reverse('yasana:landing'))
            else:
                return render(request, 'account/login.html', {'login_form': form,
                                                              'error_message': 'Invalid username or password.'})
        else:
            return render(request, 'account/login.html', {'login_form': form})


def signout(request):
    if request.user and request.user.is_authenticated():
        logout(request)

    return redirect(reverse('account:login'))


