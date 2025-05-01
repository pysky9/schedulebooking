from django.urls import path
from cart import views
from cart.api_views import *

urlpatterns = [
    # 購物車 API
    path('booking/', booking_api, name='api_booking'),
    path('add_to_cart/', add_to_cart_api, name='api_add_to_cart'),
    path('get_cart/', get_cart_api, name='api_get_cart'),
    path('update_cart_item/', update_cart_item_api, name='api_update_cart_item'),
    path('remove_cart_item/', remove_cart_item_api, name='api_remove_cart_item'),
    path('clear_cart/', clear_cart_api, name='api_clear_cart'),
]
