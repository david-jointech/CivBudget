from django.db import models
from django import forms
from django.forms import ModelForm
from django.forms import Form
from django.contrib.auth.models import User

# Create your models here.

class Booking(models.Model):
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name


class Rate(models.Model):
    days = models.IntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    daily_value = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name

    def calculate_daily_value(self):
        self.daily_value = self.value / self.days

class BookingTotal(models.Model):
    type = models.IntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField
    user = models.ForeignKey(User)


class BookingForm(Form):
    date = forms.DateTimeField(input_formats=['%d.%m.%Y'])
    value = forms.DecimalField()
    name = forms.CharField()


class RateForm(ModelForm):
    class Meta:
        model = Rate
        fields = ['days', 'value', 'name']

