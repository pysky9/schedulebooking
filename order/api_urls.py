from django.urls import path
from order import views
from order.api_views import *

urlpatterns = [
    # 訂單 API
    path('create_order/', create_order_api, name='api_create_order'),
    path('get_orders/', get_orders_api, name='api_get_orders'),
    path('get_order_details/<int:order_id>/', get_order_details_api, name='api_get_order_details'),
    path('update_order_status/', update_order_status_api, name='api_update_order_status'),
    path('cancel_order/', cancel_order_api, name='api_cancel_order'),
]
