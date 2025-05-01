from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    # 會員 API
    path('members/', include('members.api_urls')),
    
    # 日曆 API
    path('scheduler/', include('scheduler.api_urls')),
    
    # 購物車 API
    path('cart/', include('cart.api_urls')),
    
    # 訂單 API
    path('order/', include('order.api_urls')),
    
    # 其他 API 將在實現後添加
    path('line/', include('line_service.api_urls')),
    path('admin/', admin.site.urls),
]
