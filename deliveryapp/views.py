from django.forms import formset_factory
from django.shortcuts import render

# Create your views here.
from deliveryapp.forms import PizzaForm, MultiplePizzasForm


def home(request):
    return render(request, 'pizza/home.html', {})


def order(request):
    multiple_form = MultiplePizzasForm()
    if request.method == "POST":

        filled_form = PizzaForm(request.POST)

        if filled_form.is_valid():
            note = "Thank you for ordering %s %s and %s pizza on the way" % (filled_form.cleaned_data['size'],
                                                                             filled_form.cleaned_data['topping1'],
                                                                             filled_form.cleaned_data['topping2'],)
            new_form = PizzaForm()
            context = {
                'pizzaForm': new_form,
                'note': note,
                'multiple_form': multiple_form,
            }
            return render(request, 'pizza/order.html', context)

    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaForm': form, 'multiple_form': multiple_form, })


def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzasForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    pizza_form_set = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = pizza_form_set()
    if request.method == 'POST':
        filled_formset = pizza_form_set(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note = "pizzas have been ordered"
        else:
            note = " pizzas not ordered , please try again "
        return render(request, 'pizza/pizza.html', {'note': note, 'formset': formset})

    else:
        return render(request, 'pizza/pizza.html', {'formset': formset})
