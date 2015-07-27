

from django.shortcuts import render


def manage_users(request):
    return render(request, 'account/user-management.html')