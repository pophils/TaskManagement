

from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from rest_framework import status
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
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if get_user_model().objects.count() == 0:
                if email == 'admin@admin.com' and password == 'admin':
                    get_user_model().objects.create_user(email=email, first_name='admin', password=password)
                    logged_user = authenticate(username=email, password=password)
                    login(request, logged_user)
                    logged_user.user_permissions.add(Permission.objects.get(codename='can_manage_users'))
                    return redirect(reverse('yasana:landing'))
                else:
                    return render(request, 'account/login.html', {'login_form': form,
                                                                  'error_message':
                                                                      'Please supply the default admin credentials.'})
            else:
                logged_user = authenticate(username=email, password=password)
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


def selenium_login_helper(request):
    if request.method == 'GET':
        if request.user and request.user.is_authenticated() and request.user.is_active:
            return HttpResponse('ok', status=status.HTTP_200_OK)

        form = LoginForm(data=request.GET)

        if form.is_valid():
            logged_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])

            if logged_user and logged_user.is_active:
                login(request, logged_user)
                return HttpResponse('ok', status=status.HTTP_200_OK)

    return HttpResponse('Error performing login', status=status.HTTP_400_BAD_REQUEST)


