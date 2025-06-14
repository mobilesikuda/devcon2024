from django.forms import modelformset_factory, inlineformset_factory
from django import forms
from .models import OrderModel, OrderAssortmentTableModel

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['number', 'date', 'organization'] #'uuid'

        widgets = {
            'number': forms.TextInput(attrs={'class': "form-control"}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':"form-control"}),
        }

        labels = {
            'number': 'Номер документа',
            'date': 'Дата документа',
            'organization': 'Организация',
        }

    def __init__(self, *args, **kwargs):
        org = None
        if 'org' in kwargs:
            org = kwargs.pop('org')
        super().__init__(*args, **kwargs)    
        self.fields["organization"].widget.attrs.update({"class": "form-control"})
        if org is not None:    
            self.fields["organization"].widget.attrs.update({"disabled":None});
            self.fields["organization"].widget.choices = [(org.uuid, org.name)];
            #qs = self.fields['organization'].choices.queryset
            #qs = qs[:1]
            #self.fields['organization'].choices.queryset = qs
            #self.fields["organization"].widget.choices.pop(org)
            #self.fields["organization"] = forms.ChoiceField(choices=( (org.uuid, org.name)), 
            #                       widget=forms.Select(attrs={'disabled':'disabled'})) 
     

OrderAssortFormSet = inlineformset_factory(
    OrderModel,  # Родительская модель
    OrderAssortmentTableModel,  # Модель, которая будет редактироваться через inline-формы
    fields=['assortiment','count', 'price', 'summa'],  # Поля, доступные для изменения
    extra=1,  # Количество дополнительных пустых форм
    can_delete=True, # Возможность удалять связанные объекты
    widgets={
        #'num': forms.TextInput(attrs={'class': "form-control"}),
        'assortiment': forms.Select(attrs={'class': "form-control"}),
        'count': forms.TextInput(attrs={'class': "form-control", 'onchange': 'onChange(this)'}),
        'price': forms.TextInput(attrs={'class': "form-control", 'onchange': 'onChange(this)'}),
        'summa': forms.TextInput(attrs={'class': "form-control", 'onchange': 'onChange(this)'}),
        }
)    
