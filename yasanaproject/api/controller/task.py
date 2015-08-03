

from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as api_status
from yasana.models.user_task import Task


@api_view(['GET'])
def task_summary(request):

    task_status_counts = Task.objects.values('status').annotate(count=Count('status'))

    summary_count = {'new': 0, 'pending': 0, 'completed': 0}

    for count_hash in task_status_counts:
            if count_hash['status'] == 0:
                summary_count['new'] = count_hash['count']
            elif count_hash['status'] == 1:
                summary_count['pending'] = count_hash['count']
            elif count_hash['status'] == 2:
                summary_count['completed'] = count_hash['count']

    if request.GET.get('is_admin', 0) == '1':
        users_count = get_user_model().objects.count()
        summary_count['users'] = users_count - 1  # remove admin from count

    return Response(summary_count, status=api_status.HTTP_200_OK)