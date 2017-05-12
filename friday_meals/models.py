# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from meals_project.settings import RATINGS
from friday_meals.utils import get_current_date


class Category(models.Model):
    title = models.CharField(_('Category title'), max_length=128, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return unicode(self.title)


class Meal(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(_('Meal title'), max_length=128, unique=True)
    ingredients = models.TextField(_('Ingredients'), blank=True)
    price = models.DecimalField(_('Price'), max_digits=5, decimal_places=2, default=0)
    available = models.BooleanField(_('Is it available'), default=True)
    picture = models.ImageField(_('Images of the meal'), upload_to='meal_images', blank=True)

    def __unicode__(self):
        return unicode(self.title)

class MyUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        first_name = ''
        last_name = ''
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('activated', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=100)
    email = models.EmailField(unique=True, null=True)
    activated = models.BooleanField(default=False)
    token = models.CharField(blank=False, max_length=50)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __unicode__(self):
        return unicode(self.first_name)

    def __str__(self):
        return unicode(self.first_name)

    def get_full_name(self):
        return unicode(self.first_name + " " + self.last_name)

    def get_short_name(self):
        return unicode(self.first_name)


class Order(models.Model):
    user = models.ForeignKey(User)
    meal = models.ForeignKey(Meal)
    date = models.DateField(default=get_current_date)
    weekNumber = models.IntegerField()
    comment = models.TextField(blank=True)
    rating = models.CharField(max_length=2, choices=RATINGS, blank=True)

    class Meta:
        ordering = ['-weekNumber', 'user']

    def save(self, *args, **kwargs):
        if self.date:
            self.weekNumber = self.date.isocalendar()[1]
        super(Order, self).save(*args, **kwargs)


class SubmitOrder(models.Model):
    user = models.ForeignKey(User)
    weekNumber = models.IntegerField()
    submitted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-weekNumber']
