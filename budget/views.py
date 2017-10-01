from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from dateutil import parser
from .models import *
from .utils import Utils
from django.utils import timezone
import datetime
from datetime import timedelta
from django.db.models import Sum
from graphos.sources.model import SimpleDataSource
from graphos.renderers.morris import BarChart
from collections import Counter


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# TODO add BookingTotals-functonality and remove old stuff
@login_required
def index(request):
    user = request.user
    now = timezone.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    first_day_of_month = today.replace(day=1)
    monday_of_this_week = today - timedelta(days=today.weekday())
    rate_list = Rate.objects.filter(user=user).order_by('daily_value')
    # TODO refactor this mess!
    bookings_of_day = Booking.objects.filter(user=user).order_by('value').filter(date__range=[today, now])
    bookings_of_week = Booking.objects.filter(user=user).order_by('value').filter(
         date__range=[monday_of_this_week, now]).aggregate(balance_of_week=Sum('value'))
    bookings_of_month = Booking.objects.filter(user=user).order_by('value').filter(
        date__range=[first_day_of_month, now]).aggregate(balance_of_month=Sum('value'))
    bookings_forever =  Booking.objects.filter(user=user).aggregate(balance_forever=Sum('value'))
    bookings = Booking.objects.filter(user=user).order_by('date')
    start_date = bookings[0].date
    end_date = today
    #aggregated_by_day = [['Date', 'Value']]
    #for single_date in daterange(start_date, end_date):
    #    bookings_up_to_day = Booking.objects.filter(user=user).filter(
    #        date__range=[start_date, single_date]).aggregate(
    #        balance_up_to_day=Sum('value'))['balance_up_to_day']
    #    aggregated_by_day.append([single_date, bookings_up_to_day])
    #data_source = SimpleDataSource(aggregated_by_day)
    #chart = BarChart(data_source)
    context = {
        'bookings_of_day': bookings_of_day,
        'rate_list': rate_list,
        'magic_number': Utils.calculate_daily_rate(rate_list),
        'booking_total': Utils.calculate_total(bookings_of_day),
        'today': timezone.now(),
        'balance_of_week': bookings_of_week['balance_of_week'],
        'balance_of_month': bookings_of_month['balance_of_month'],
        'balance_forever': bookings_forever['balance_forever'],
     #   'chart': chart,

    }
    return render(request, 'budget/index.html', context)


@login_required
def add_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = Booking(name=form.cleaned_data['name'], value=form.cleaned_data['value'],
                              date=form.cleaned_data['date'], user=request.user)
            booking.save()
    return redirect('/')


@login_required
def add_rate(request):
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = Rate(name=form.cleaned_data['name'], value=form.cleaned_data['value'],
                        days=form.cleaned_data['days'], user=request.user)
            rate.calculate_daily_value()
            rate.save()
    return redirect('/')


@login_required
def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.delete()
    return redirect('/')


@login_required
def delete_rate(request, rate_id):
    rate = Rate.objects.get(id=rate_id)
    rate.delete()
    return redirect('/')
