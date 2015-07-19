

from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, max_length=255,
                             error_messages={'required': 'Please enter your email address.'})
    password = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput,
                               error_messages={'required': 'Please enter your password.'})

    class Meta:
        fields = ('email', 'password')
        error_messages = {
            'email': {'required': 'Please enter your email address.'},
            'password': {'required': 'Please enter your password.'},
        }


