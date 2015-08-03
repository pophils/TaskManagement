

from django import forms


class EditUserForm(forms.Form):

    Gender_Choices = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('p', 'Prefer not to say')
    )

    email = forms.EmailField(required=True, max_length=255)
    first_name = forms.CharField(required=True, max_length=255)
    other_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)
    department = forms.CharField(max_length=255, required=False)
    phone = forms.CharField(max_length=255, required=False)
    website = forms.URLField(max_length=255, required=False)
    gender = forms.CharField(max_length=1, required=True)

    class Meta:
        fields = ('first_name', 'last_name', 'other_name', 'phone', 'gender', 'department',
                  'website', 'email')
        error_messages = {
            'email': {'required': 'Please enter email address.', 'invalid': 'Please enter a valid email address.'},
            'first_name': {'required': 'Please enter first name.'},
            'gender': {'required': 'Please select a gender.', 'invalid_choice': 'Please select a valid gender.'},
        }


