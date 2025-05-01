from django.urls import path
from scheduler import views
from scheduler.api_views import *

urlpatterns = [
    # 日曆數據 API
    path('time_periods/', time_periods_api, name='api_time_periods'),
    path('time_prices/', time_prices_api, name='api_time_prices'),
    path('reservation_times/', reservation_times_api, name='api_reservation_times'),
    path('consumer_data/', consumer_data_api, name='api_consumer_data'),
    
    # 商家時間設置 API
    path('merchant_time_slots/', merchant_time_slots_api, name='api_merchant_time_slots'),
    path('merchant_time_slots/update/', update_merchant_time_slots_api, name='api_update_merchant_time_slots'),
    path('merchant_time_slots/delete/', delete_merchant_time_slots_api, name='api_delete_merchant_time_slots'),
]
