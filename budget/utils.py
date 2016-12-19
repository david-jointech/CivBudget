from decimal import Decimal


class Utils:

    @staticmethod
    def calculate_daily_rate(rate_list):
        daily_rate = Decimal(0)
        for rate in rate_list:
            daily_rate += rate.daily_value
        return daily_rate

    @staticmethod
    def calculate_total(booking_list):
        total = Decimal(0)
        for booking in booking_list:
            total += booking.value
        return total

