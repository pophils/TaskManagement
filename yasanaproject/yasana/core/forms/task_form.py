

from django import forms
from yasana.models import Task


class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('title', 'details', 'priority', 'start_date', 'expected_end_date')
        error_messages = {
            'title': {'required': 'Please enter task title.'},
            'details': {'required': 'Please enter task details.'},
            'priority': {'required': 'Please select a priority.', 'invalid_choice': 'Please select a valid priority.'},
        }
