from multiprocessing import context
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Pizza, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from deliveryapp.forms import PizzaForm, MultiplePizzasForm, CreateUserForm


def home(request):
    return render(request, 'pizza/home.html', {})


@login_required(login_url='login')
def order(request):
    multiple_form = MultiplePizzasForm()
    if request.method == "POST":
        filled_form = PizzaForm(request.POST)

        if filled_form.is_valid():
            filled_form.instance.user = request.user
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = "Thank you for ordering %s %s and %s , your pizza is  on the way" % (
                filled_form.cleaned_data['size'],
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == "POST":
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = "order has been updated"
            return render(request, 'pizza/edit_order.html', {'note': note, 'pizzaform': form, 'pizza': pizza})
    return render(request, 'pizza/edit_order.html', {'pizzaform': form, 'pizza': pizza})


@login_required(login_url='login')
def orders(request):
    orders = Pizza.objects.all()
    filtered_orders = orders.filter(user=request.user)
    context = {
        'orders': filtered_orders
    }
    return render(request, 'pizza/orders.html', context)


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            note = " Login successful"
            context = {
                'note': note
            }
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')
            note = "Incorrect username or password"
            context = {
                'note': note
            }
            return render(request, 'pizza/login.html', context)

    context = {}
    return render(request, 'pizza/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'pizza/register.html', context)


def deleteorder(request, pk):
    orders = Pizza.objects.get(id=pk)
    orders.delete()
    return HttpResponseRedirect(reverse('orders'))
def oder_details(request , pk):
    order_details = Pizza.objects.get(pk =id)
    context = {
        'details' : oder_details

    }
    return render(request)
def profile(request):
    profile_details = User.objects.get(id)
    context = {
        'user': profile_details
    }
    return render(request, 'pizza/base.html', context)

