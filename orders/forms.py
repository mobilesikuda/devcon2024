from django.forms import modelformset_factory, inlineformset_factory
from django import forms
from .models import OrderModel, OrderAssortmentTableModel
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['number', 'date', 'organization','comment'] 

        widgets = {
            'number': forms.TextInput(attrs={'class': "form-control"}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':"form-control"}),
        }

        labels = {
            'number': 'Номер документа',
            'date': 'Дата документа',
            'organization': 'Организация',
            'comment': 'Коментарий',
        }

    def __init__(self, *args, **kwargs):
        org = None
        if 'org' in kwargs:
            org = kwargs.pop('org')
        super().__init__(*args, **kwargs)    
        self.fields["organization"].widget.attrs.update({"class": "form-select"})
        self.fields["number"].widget.attrs.update({"class": "text-start"})
        self.fields["date"].widget.attrs.update({"class": "text-end"})
        self.fields["comment"].widget.attrs.update({"class": "w-100"})
        if org is not None:    
            self.fields["organization"].widget.attrs.update({"disabled":None});
            self.fields["organization"].widget.choices = [(org.uuid, org.name)];

OrderAssortFormSet = inlineformset_factory(
    OrderModel,  # Родительская модель
    OrderAssortmentTableModel,  # Модель, которая будет редактироваться через inline-формы
    fields=['assortiment','count', 'price', 'summa'],  # Поля, доступные для изменения
    extra=1,  # Количество дополнительных пустых форм
    can_delete=True, # Возможность удалять связанные объекты
    widgets={
        'assortiment': forms.Select(attrs={'class': "form-select"}),
        'count': forms.TextInput(attrs={'class': "form-control text-end", 'onchange': 'onChange(this)'}),
        'price': forms.TextInput(attrs={'class': "form-control text-end", 'onchange': 'onChange(this)'}),
        'summa': forms.TextInput(attrs={'class': "form-control text-end", 'onchange': 'onChange(this)'}),
        }
)    
