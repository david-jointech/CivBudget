from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from dateutil import parser
from .models import *
from .utils import Utils
from django.utils import timezone


@login_required
def index(request):
    user = request.user
    now = timezone.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    rate_list = Rate.objects.filter(user=user).order_by('daily_value')
    booking_list = Booking.objects.filter(user=user).order_by('value').filter(date__range=[today, now])
    context = {
        'booking_list': booking_list,
        'rate_list': rate_list,
        'magic_number': Utils.calculate_daily_rate(rate_list),
        'booking_total': Utils.calculate_total(booking_list),
        'today': timezone.now(),
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
                              days=parser.parse(form.cleaned_data['days']), user=request.user)
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
