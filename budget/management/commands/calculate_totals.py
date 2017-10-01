from django.core.management.base import BaseCommand, CommandError
from budget.utils import Utils
from budget.models import *
from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = 'Recalculates the BookingTotals'

    def handle(self, *args, **options):
        now = timezone.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        for user in User.objects.all():
            self.calculate_totals_for_type(today, user, DAILY)
            self.calculate_totals_for_type(today, user, WEEKLY)
            self.calculate_totals_for_type(today, user, MONTHLY)
            self.calculate_totals_for_type(today, user, YEARLY)
            self.cleanUp()

    def calculate_totals_for_type(self, today, user, type):
        curr_date = today
        # TODO write helperfunctions
        while (isAllowed(today, curr_date, type)):
            self.calculate_single_total(curr_date, type, user)

    def calculate_single_total(self, curr_date, type, user):
        # TODO sum up directly
        # TODO get Start and End Date
        booking_sum = Booking.objects.filter(user=user,
                                             date__range=[getStartDate(curr_date, type), getEndDate(curr_date, type)])
        # Write enum
        total = BookingTotal.objects.filter(date=curr_date, type=type, user=user)
        if not total.exists():
            total = BookingTotal(date=curr_date, type=type, value=booking_sum, user=user)
            total.save()
        elif booking_sum != total.value:
            total.value = booking_sum
            total.save()

    def cleanUp(self):
        # TODO implement
        