

from django.shortcuts import render


def task_collection_partial(request):
    status = request.GET.get('status', None)

    if status:
        status = int(status)
        if status == 0:
            return render(request, 'partials/task_collection.html')
