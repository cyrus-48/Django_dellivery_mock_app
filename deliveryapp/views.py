from django.shortcuts import render


# Create your views here.
from deliveryapp.forms import PizzaForm


def home(request):
    return render(request, 'pizza/home.html', {})


def order(request):
    if request.method == "POST":

        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            note = "Thank you for ordering %s %s and %s pizza on the way"  %(filled_form.cleaned_data['size'],
            filled_form.cleaned_data['topping1'],
            filled_form.cleaned_data['topping2'],)
            new_form = PizzaForm()
            context = {
                'pizzaForm':new_form,
                'note':note,
            }
            return render(request, 'pizza/order.html', context)

    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaForm':form})
