from django.core.management.base import BaseCommand, CommandError
from budget.utils import Utils
from budget.models import *
from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = 'Books the magic number'

    def handle(self, *args, **options):
        now = timezone.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        magic_number_string = "Magic Number"
        for user in User.objects.all():
            booking = Booking.objects.filter(user=user, name=magic_number_string,date__range=[today, today])
            if not booking.exists():
                rate_list = Rate.objects.filter(user=user)
                magic_number = Utils.calculate_daily_rate(rate_list)
                booking = Booking(name=magic_number_string, date=today, value=magic_number, user=user)
                booking.save()
