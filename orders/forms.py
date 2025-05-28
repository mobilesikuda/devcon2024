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



# Основная форма для модели Author
class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['uuid','number', 'date', 'organization']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

        labels = {
            'number': 'Номер документа',
            'date': 'Дата документа',
            'organization': 'Организация',
        }

# Inline-formset для модели Book
OrderAssortFormSet = inlineformset_factory(
    OrderModel,  # Родительская модель
    OrderAssortmentTableModel,  # Модель, которая будет редактироваться через inline-формы
    fields=['num','assortiment','count'],  # Поля, доступные для изменения
    extra=1,  # Количество дополнительных пустых форм
    can_delete=True  # Возможность удалять связанные объекты
)    
