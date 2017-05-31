from datetime import datetime
from .models import Meal

CURRENT_WEEK = datetime.now().isocalendar()[1]


def get_current_week():
    return datetime.now().isocalendar()[1]

def get_searched_meals(string=''):
    meals_list = []
    if string:
        meals_list = Meal.objects.filter(title__icontains=string)
    return meals_list