

from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as api_status
from yasana.models.user_task import Task
from yasana.core.serializers.task_serializer import TaskSerializer
from yasana.core.forms.task_form import CreateTaskForm


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


@api_view(['GET'])
def get_task_total_count(request):

    status = request.GET.get('status')
    if status is None:
            return Response({'message': 'bad request, pass a status query parameter'},
                            status=api_status.HTTP_400_BAD_REQUEST)
    try:
        status = int(status)
    except ValueError:
        return Response({'message': 'bad request, pass a status query parameter'},
                        status=api_status.HTTP_400_BAD_REQUEST)

    if status == 0:
        num_of_tasks = Task.objects.filter(status=0).count()
    else:
        num_of_tasks = Task.objects.filter(status=1).count()

    return Response({'num_of_tasks': num_of_tasks}, status=api_status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def api_get_tasks(request):

    if request.method == 'GET':
        try:
            page_num = int(request.GET.get('pg_no', 0))
            status = int(request.GET.get('status', None))
        except TypeError:
            return Response({'status': 'bad request'}, status=api_status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'status': 'bad request'}, status=api_status.HTTP_400_BAD_REQUEST)

        if page_num < 0:
            page_num = 0
        if status < 0:
            status = 0
        elif status > 1:
            status = 1

        tasks = Task.objects.filter(status=status)
        return Response(TaskSerializer(tasks.order_by('-created_date')[page_num:page_num+10], many=True)
                        .data, status=api_status.HTTP_200_OK)

    elif request.method == 'POST':
        form = CreateTaskForm(data=request.data)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return Response({'save_status': True, 'id': task.id}, status=api_status.HTTP_200_OK)
        return Response({'save_status': form.errors}, status=api_status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            pk = int(request.data['id'])
        except KeyError:
            return Response({'status': 'bad request'}, status=api_status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'status': 'bad request'}, status=api_status.HTTP_400_BAD_REQUEST)

        form = CreateTaskForm(data=request.data)

        if form.is_valid():
            task = Task.objects.filter(pk=pk)
            task.update(**form.cleaned_data)
            return Response({'save_status': True}, status=api_status.HTTP_200_OK)
        return Response({'save_status': form.errors}, status=api_status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        try:
            pk = int(request.data['id'])
        except KeyError:
            return Response({'status': 'bad request'}, status=api_status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'status': 'bad request'}, status=api_status.HTTP_400_BAD_REQUEST)

        task = Task.objects.filter(pk=pk)

        if task:
            task.delete()
            return Response({'save_status': True}, status=api_status.HTTP_200_OK)

        return Response({'save_status': False}, status=api_status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def api_complete_task(request):

    try:
        pk = int(request.data['id'])
    except KeyError:
        return Response({'status': 'bad request'}, status=api_status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'status': 'bad request'}, status=api_status.HTTP_400_BAD_REQUEST)

    task = Task.objects.filter(pk=pk)

    if task:
        task.update(status=1, is_completed=True)
        return Response({'status': True}, status=api_status.HTTP_200_OK)



