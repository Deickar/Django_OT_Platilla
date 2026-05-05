from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label='Nombre',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name  = forms.CharField(max_length=150, required=True, label='Apellido',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    email      = forms.EmailField(required=True, label='Correo',
                                   widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserEditForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'is_staff']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff':   forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
