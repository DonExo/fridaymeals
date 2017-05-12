# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category, Meal, User, Order, SubmitOrder

class AdminCategory(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

class AdminMeal(admin.ModelAdmin):
    list_display = ['title', 'category', 'price']
    search_fields = ['title']

class AdminUser(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'activated']
    search_fields = ['email']

class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'user', 'meal', 'date', 'comment', 'weekNumber']

class AdminSubmitOrder(admin.ModelAdmin):
    list_display = ['weekNumber', 'user', 'submitted']

admin.site.register(Category, AdminCategory)
admin.site.register(Meal, AdminMeal)
admin.site.register(User, AdminUser)
admin.site.register(Order, AdminOrder)
admin.site.register(SubmitOrder, AdminSubmitOrder)