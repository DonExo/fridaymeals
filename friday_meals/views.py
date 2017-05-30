# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.db.models import Count
from .models import User, Meal, Category, Order, SubmitOrder
from .forms import UserRegisterForm, MealPickForm, LoginForm
from .utils import CURRENT_WEEK
from .emails import notify_user_deleted_meal, notify_staff_to_order, send_user_token
from uuid import uuid4
import json


def index(request):
    return render(request, 'friday_meals/index.html')


def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.activated:
                    login(request, user)
                    messages.success(request, "Logged-in!")
                    return HttpResponseRedirect(reverse('profile'))
                else:
                    messages.info(request, "Activate your account! (Check your email for activation link)")
                    return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, "Invalid credentials!")
                return HttpResponseRedirect(reverse('login'))
    else:
        if request.user.is_authenticated:
            messages.info(request, "You are already logged-in!")
            return HttpResponseRedirect(reverse('profile'))

        login_form = LoginForm()

    return render(request, 'friday_meals/login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged-out!")
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            token = uuid4().int
            user.token = token
            user.save()
            token = "{}-{}".format(token, user.id)
            send_user_token(token, user)
            messages.success(request, "An e-mail has been sent to activate your account!")
            return HttpResponseRedirect(reverse('index'))
    else:
        if request.user.is_authenticated:
            messages.info(request, "You are already registered and logged in!")
            return HttpResponseRedirect(reverse('profile'))
        user_form = UserRegisterForm()

    return render(request, 'friday_meals/register.html', {'user_form': user_form, 'title': 'Register'})


def activate_token(request, token):
    user_id = str(token).split('-')[1]
    token = str(token).split('-')[0]
    user = User.objects.filter(id=user_id).first()
    if user:
        if user.token == token:
            if not user.activated:
                user.activated = True
                user.save()
                messages.success(request, "You have successfully activated your account!")
                messages.success(request, "Please log in to start...")
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.info(request, "Your account is already activated!")
                return HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(request, "Invalid token credentials!")
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, "Invalid token credentials! (No such user)")
        return HttpResponseRedirect(reverse('index'))


@login_required()
def profile(request):
    meal_pick = MealPickForm()
    dictionary = {'title': "Profile", 'meal_pick': meal_pick}
    order_submitted = False
    current_week_meals = Order.objects.filter(user=request.user, weekNumber=CURRENT_WEEK)

    if current_week_meals:  # Zemi gi site meals za tekovnata nedela za korisnikot
        # order_submitted = True ###  Un-comment this if you want to allow only one meal per person
        dictionary.update({'picked_meal': current_week_meals})

    check_submitted = SubmitOrder.objects.filter(weekNumber=CURRENT_WEEK).first()

    if check_submitted:
        if check_submitted.submitted:
            order_submitted = True

    dictionary['submitted'] = order_submitted

    previous_weeks_meals = Order.objects.filter(user=request.user).exclude(weekNumber=CURRENT_WEEK).order_by('-weekNumber')
    if previous_weeks_meals:
        dictionary.update({'previous_meals': previous_weeks_meals})

    if request.method == "POST":
        meal = request.POST['meals']
        comment = request.POST['comment']
        order = Order(user=request.user, meal_id=meal, comment=comment)
        order.save()
        messages.success(request, "Meal picked!")
        return HttpResponseRedirect(reverse('profile'))

    return render(request, 'friday_meals/profile.html', dictionary)


@login_required
@staff_member_required
def admin_panel(request):

    orders_list = {}
    suma = 0
    get_all_orders = Order.objects.filter(weekNumber=CURRENT_WEEK)
    for order in get_all_orders:
        suma += order.meal.price

    aggregated_query = Order.objects.filter(weekNumber=CURRENT_WEEK).values('meal__title').annotate(total=Count('meal_id'))
    aggregated_list = {entry['meal__title']: entry['total'] for entry in aggregated_query}

    orders_list.update({'orders': get_all_orders, 'suma': suma, 'aggregated_orders': aggregated_list})

    order = SubmitOrder.objects.filter(weekNumber=CURRENT_WEEK).first()
    if order:
        if order.submitted:
            orders_list.update({'order_disabled': 'order_disabled'})

    return render(request, 'friday_meals/admin.html', orders_list)


def meal_details(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    return render(request, 'friday_meals/meal.html', {
        'meal': meal,
        'title': "Meal view"
    })


def categories(request):
    return render(request, 'friday_meals/categories.html', {'title': 'All categories'})


def category_items(request, category_id):
    category = Category.objects.filter(id=category_id).first()
    if not category:
        messages.error(request, "There is no such category!")
        return HttpResponseRedirect(reverse('category'))

    meals = Meal.objects.filter(category=category_id)
    dictionary = {'category': category, 'meals': meals, 'title': 'In category view'}

    return render(request, 'friday_meals/category_items.html', dictionary)


def assign_category(request):
    meals_list = None
    if 'category' in request.GET:
        category = request.GET['category']
        cat = Category.objects.get(id=category)
        meals = Meal.objects.filter(category=cat)

        meals_list = {meal.id: meal.title for meal in meals}

    return HttpResponse(json.dumps(meals_list))


def get_searched_meals(string=''):
    meals_list = []
    if string:
        meals_list = Meal.objects.filter(title__icontains=string)

    return meals_list


def search_meals(request):
    meals_list = []
    if 'meal_title' in request.GET:
        string = request.GET['meal_title']
        meals_list = get_searched_meals(string)

    return render(request, 'friday_meals/search_meal.html', {'meals_list': meals_list})


def reset_meal(request):
    referer = None
    if 'HTTP_REFERER' in request.META:
        referer = request.META['HTTP_REFERER']

    if referer and referer.rsplit('/', 2)[1] == 'profile':

        query = Order.objects.filter(user=request.user, weekNumber=CURRENT_WEEK)
        if query:
            for entry in query:
                entry.delete()
        else:
            messages.info(request, "You haven't submitted your lunch yet!")
            return HttpResponseRedirect(reverse('profile'))

        messages.info(request, "Pick your lunch again!")
        return HttpResponseRedirect(reverse('profile'))
    else:
        messages.error(request, "You can't access this page like that!")
        return HttpResponseRedirect(reverse('index'))


@login_required
@staff_member_required
def send_order_to_staff(request):
    referer = None
    if 'HTTP_REFERER' in request.META:
        referer = request.META['HTTP_REFERER']

    if referer and referer.rsplit('/', 2)[1] == 'admin-panel':  # Check if the button was clicked from the ADMIN PROFILE panel otherwise don't do it
        all_meals_query = Order.objects.filter(weekNumber=CURRENT_WEEK)

        suma = 0
        for order in all_meals_query:
            suma += order.meal.price
        lista = [meal for meal in all_meals_query]

        notify_staff_to_order(lista, suma)  # Email notification to staff member

        ordered = SubmitOrder.objects.filter(weekNumber=CURRENT_WEEK)  # Check if is an order for the current week (added ability to "Undo" order)
        if ordered:
            ordered.update(submitted=True)  # If it is, submit it / lock it
        else:
            new_order = SubmitOrder(user=request.user, weekNumber=CURRENT_WEEK, submitted=True)
            new_order.save()  # if there isn't, make one

        messages.success(request, "Orders sent to staff!")

    else:  # If not clicked from the PROFILE ADMIN button
        messages.error(request, "You can't access this page like that!")
        return HttpResponseRedirect(reverse('index'))

    return HttpResponseRedirect(reverse('admin_panel'))


@login_required
@staff_member_required
def admin_undo_order(request):
    referer = None
    if 'HTTP_REFERER' in request.META:
        referer = request.META['HTTP_REFERER']

    if referer and referer.rsplit('/', 2)[1] == 'admin-panel':
        ordered = SubmitOrder.objects.filter(weekNumber=CURRENT_WEEK).first()
        if ordered:
            if ordered.submitted:
                ordered.submitted = False
                ordered.save()
                messages.info(request, "Order undo-ed! ")
    else:  # If not clicked from the PROFILE ADMIN button
        messages.error(request, "You can't access this page like that!")
        return HttpResponseRedirect('/')
    return HttpResponseRedirect(reverse('admin_panel'))


@login_required()
def delete_meal_from_order(request, meal_id):
    if 'HTTP_REFERER' not in request.META:
        messages.error(request, "You can't access this page like that!")
        return HttpResponseRedirect(reverse('index'))

    referer = request.META['HTTP_REFERER'].rsplit('/', 2)[1]

    to_delete = Order.objects.filter(id=meal_id).first()
    if to_delete:
        to_delete.delete()
        messages.success(request, "Meal deleted successfully from order!")
    if referer == 'profile':
        return HttpResponseRedirect(reverse('profile'))
    else:
        notify_user_deleted_meal(to_delete.user)  # Notify user that his meal was deleted
        return HttpResponseRedirect(reverse('admin_panel'))
