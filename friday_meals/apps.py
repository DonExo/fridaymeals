# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

class FridayMealsConfig(AppConfig):
    name = 'friday_meals'

    def ready(self):
        from friday_meals.signals import *