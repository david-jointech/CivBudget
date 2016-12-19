from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_booking$', views.add_booking, name='add_booking'),
    url(r'^add_rate', views.add_rate, name='add_rate'),
    url(r'^delete_booking/(?P<booking_id>[0-9]+)/$', views.delete_booking, name='delete_booking'),
    url(r'^delete_rate/(?P<rate_id>[0-9]+)/$', views.delete_rate, name='delete_rate'),
    url(r'^login$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
