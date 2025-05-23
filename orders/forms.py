from django import forms
from .models import OrderModel

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['uuid', 'number', 'organization']
        # widgets = {
        #     'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        #     'category': forms.Select(choices=[('a', 'Option A'), ('b', 'Option B')]),
        # }
        labels = {
            'number': 'Номер документа',
            'organization': 'Организация',
        }
        # initial = {
        #     'category': 'b',
        # }
    # uuid = forms.UUIDField(required=True)
    # number = forms.CharField(max_length=50,label="Номер документа")
    # date = forms.DateTimeField(label="Дата документа")
    # organization = forms.ForeignKey(OrganizationModel)
