

from rest_framework import serializers
from yasana.models.user_task import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('title', 'details', 'priority', 'start_date', 'expected_end_date', 'id')

