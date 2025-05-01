from django.urls import path
from members import views
from members.api_views import *

urlpatterns = [
    # 用戶認證 API
    path('login/', login_api, name='api_login'),
    path('register/', register_api, name='api_register'),
    path('logout/', logout_api, name='api_logout'),
    path('profile/', profile_api, name='api_profile'),
    path('update_profile/', update_profile_api, name='api_update_profile'),
    path('change_password/', change_password_api, name='api_change_password'),
    path('check_auth/', check_auth_api, name='api_check_auth'),
]