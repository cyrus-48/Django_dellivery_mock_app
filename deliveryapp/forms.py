from  django import  forms
class PizzaForm(forms.Form):
    topping1 = forms.CharField(label='topping 1', max_length=100)
    topping2 = forms.CharField(label='topping 2', max_length=100)
    size = forms.ChoiceField(label='size' , choices=[('small','small'),('medium' , 'medium'),('large','large') ])
