

from django.contrib.auth import get_user_model
from django import forms
from ..validators import validate_user_phone_no


class CreateUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = True
        self.fields['phone'].validators.append(validate_user_phone_no)

    confirm_password = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput,
                                       error_messages={'required': 'Please confirm entered password.'})

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'other_name', 'phone', 'gender', 'department',
                  'website', 'email', 'password', 'confirm_password')
        error_messages = {
            'email': {'required': 'Please enter email address.', 'invalid': 'Please enter a valid email address.'},
            'password': {'required': 'Please enter password.'},
            'first_name': {'required': 'Please enter first name.'},
            'gender': {'required': 'Please select a gender.', 'invalid_choice': 'Please select a valid gender.'},
        }

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password', None)
        password = self.cleaned_data.get('password', None)

        if confirm_password and password:
            if confirm_password == password:
                return confirm_password

        raise forms.ValidationError('Password confirmation does not match.')

    def clean_email(self):
        email = self.cleaned_data.get('email', None)

        if email:
            if not get_user_model().objects.filter(email=email.strip()).exists():
                return email

        raise forms.ValidationError('Please enter a new email address, email already exist.')
