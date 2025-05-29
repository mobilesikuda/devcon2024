from django.forms import modelformset_factory, inlineformset_factory
from django import forms
from .models import OrderModel, OrderAssortmentTableModel

# class OrderForm(forms.Form): #ModelForm
#     # class Meta:
#     #     model = OrderModel
#     #     fields = ['uuid', 'number', 'organization']
#     #     # widgets = {
#     #     #     'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
#     #     #     'category': forms.Select(choices=[('a', 'Option A'), ('b', 'Option B')]),
#     #     # }
#     #     labels = {
#     #         'number': 'Номер документа',
#     #         'organization': 'Организация',
#     #     }
#     #     # initial = {
#     #     #     'category': 'b',
#     #     # }
#     uuid = forms.UUIDField(required=True)
#     number = forms.CharField(max_length=50,label="Номер документа")
#     date = forms.DateTimeField(label="Дата документа")
#     organization = forms.CharField()



class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['uuid','number', 'date', 'organization']

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
        super().__init__(*args, **kwargs)
        self.fields["organization"].widget.attrs.update({"class": "form-control"})

OrderAssortFormSet = inlineformset_factory(
    OrderModel,  # Родительская модель
    OrderAssortmentTableModel,  # Модель, которая будет редактироваться через inline-формы
    fields=['num','assortiment','count'],  # Поля, доступные для изменения
    extra=1,  # Количество дополнительных пустых форм
    can_delete=False  # Возможность удалять связанные объекты

)    
