from django import forms
from .models import *


# class PizzaForm(forms.Form):
#     topping1 = forms.CharField(label='topping 1', max_length=100)
#     topping2 = forms.CharField(label='topping 2', max_length=100)
#     size = forms.ChoiceField(label='size' , choices=[('small','small'),('medium' , 'medium'),('large','large') ])
class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['topping1', 'topping2', 'size']
        labels = {'topping1': 'Topping 1', 'topping2': 'Topping 2'}


class MultiplePizzasForm(forms.Form):
    number = forms.IntegerField(min_value=2, max_value=8)
