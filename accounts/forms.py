from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        label='Nome Completo'
    )
    date_of_birth = forms.DateField(
        required=True,
        label='Data de Nascimento',
        widget=forms.DateInput(format='%d/%m/%Y')  
    )
    email = forms.EmailField(
        required=True,
        label='E-mail'
    )

    class Meta:
        model = CustomUser 
        fields = ['username', 'full_name', 'date_of_birth', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.email = self.cleaned_data['email']
        if commit:
            user.save() 
        return user
    

class PortugueseDateInput(forms.DateInput):
    input_type = 'date'
    format = '%d/%m/%Y' 

    def __init__(self, *args, **kwargs):
        kwargs['format'] = self.format
        super().__init__(*args, **kwargs)