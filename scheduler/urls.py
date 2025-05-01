from django.urls import path
from scheduler import views

app_name = "scheduler"

urlpatterns = [
    path('views/<storename>', views.calendar, name='calendar'),
    path('setting/', views.calendar_setting, name='calendar_setting'),
    path('response_period/', views.response_time_period, name='response_time_period'),
    path('response_time_price/', views.response_time_price, name='response_time_price'),
    path('booked_calendar/<storename>', views.booked_calendar, name='booked_calendar'),
    path('time_setting_records/<storename>', views.time_setting_records, name='time_setting_records'),
    path('get_reservation_time/', views.get_reservation_time, name='get_reservation_time'),
    path('get_consumer_data/', views.get_consumer_data, name='get_consumer_data'),
    path('fetch_merchant_time_slots/', views.fetch_merchant_time_slots, name='fetch_merchant_time_slots'),
    path('update_merchant_time_slots/', views.update_merchant_time_slots, name='update_merchant_time_slots'),
    path('delete_merchant_time_slots/', views.delete_merchant_time_slots, name='delete_merchant_time_slots')
]
