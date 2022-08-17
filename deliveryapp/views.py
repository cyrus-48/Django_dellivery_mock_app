from django.forms import formset_factory
from django.shortcuts import render
from .models import Pizza

# Create your views here.
from deliveryapp.forms import PizzaForm, MultiplePizzasForm


def home(request):
    return render(request, 'pizza/home.html', {})


def order(request):
    multiple_form = MultiplePizzasForm()
    if request.method == "POST":

        filled_form = PizzaForm(request.POST)

        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = "Thank you for ordering %s %s and %s pizza on the way" % (filled_form.cleaned_data['size'],
                                                                             filled_form.cleaned_data['topping1'],
                                                                             filled_form.cleaned_data['topping2'],)
            new_form = PizzaForm()
            context = {
                'pizzaForm': new_form,
                'note': note,
                'multiple_form': multiple_form,
                'created_pizza_pk': created_pizza_pk,
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


def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == "POST":
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = "order has been updated"
            return render(request, 'pizza/edit_order.html', {'note':note,'pizzaform': form, 'pizza': pizza})
    return render(request , 'pizza/edit_order.html',{'pizzaform':form,'pizza':pizza})
