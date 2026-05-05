from django import forms
from django.contrib.auth.models import User
from .models import WorkOrder


class WorkOrderForm(forms.ModelForm):
    """Formulario para crear y editar órdenes de trabajo."""

    class Meta:
        model = WorkOrder
        fields = ['title', 'description', 'status', 'priority', 'assigned_to', 'due_date']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la orden'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción detallada'}),
            'status':      forms.Select(attrs={'class': 'form-select'}),
            'priority':    forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'due_date':    forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
        self.fields['assigned_to'].empty_label = '— Sin asignar —'
        self.fields['due_date'].required = False


class WorkOrderFilterForm(forms.Form):
    """Formulario de filtros para el listado de órdenes."""

    status   = forms.ChoiceField(required=False, label='Estado',
                                  choices=[('', 'Todos')] + WorkOrder.Status.choices,
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    priority = forms.ChoiceField(required=False, label='Prioridad',
                                  choices=[('', 'Todas')] + WorkOrder.Priority.choices,
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    assigned_to = forms.ModelChoiceField(required=False, label='Asignado a',
                                          queryset=User.objects.filter(is_active=True),
                                          empty_label='Todos',
                                          widget=forms.Select(attrs={'class': 'form-select'}))
    search = forms.CharField(required=False, label='Buscar',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por código o título...'}))
