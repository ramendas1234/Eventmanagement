from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name', widget=forms.TextInput(attrs={'placeholder':'Enter First Name'}))
    last_name = forms.CharField(max_length=100, help_text='Last Name', widget=forms.TextInput(attrs={'placeholder':'Enter Last Name'}))
    email = forms.EmailField(max_length=150, help_text='Email',widget=forms.TextInput(attrs={'placeholder':'Enter Email'}))
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Enter Confirm Password'    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
'email', 'password1', 'password2',)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
        }

        