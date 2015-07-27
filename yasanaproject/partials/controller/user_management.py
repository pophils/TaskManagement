

from django.shortcuts import render


def user_collection_partial(request):
    return render(request, 'partials/user_collection.html')


def add_user_partial(request):
    return render(request, 'partials/add_user.html')

