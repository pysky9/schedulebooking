from datetime import date, datetime, time
import json
import jwt
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction

from members.models import Members
from scheduler.models import Time_setting, Time_pricing
from cart.models import Booking
from order.models import Order
from scheduler.views import (
    convert_date_to_datetime, check_overlap, 
    generate_time_slice, time_slice_format, 
    convert_to_datetime
)

time_setting = Time_setting()
time_pricing = Time_pricing()

# 獲取 JWT 密鑰
jwt_key = os.getenv("jwt_key")

# 驗證 JWT 令牌的裝飾器
def jwt_auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        jwt_token = request.COOKIES.get("jwt_token") or request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not jwt_token:
            return JsonResponse({"success": False, "message": "未授權訪問，請先登錄"}, status=401)
        
        try:
            payload = jwt.decode(jwt_token, jwt_key, algorithms=["HS256"])
            request.user_id = payload.get("id")
            request.user_email = payload.get("email")
        except jwt.ExpiredSignatureError:
            return JsonResponse({"success": False, "message": "登錄已過期，請重新登錄"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"success": False, "message": "無效的登錄憑證"}, status=401)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

# 時間段 API
@require_http_methods(["GET", "POST"])
@csrf_exempt
@jwt_auth_required
def time_periods_api(request):
    """獲取或設置時間段"""
    if request.method == "GET":
        try:
            user_id = request.user_id
            member = Members.objects.get(id=user_id)
            
            time_periods = time_setting.get_time_period(member.id)
            
            return JsonResponse({
                "success": True,
                "time_periods": time_periods
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=400)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = request.user_id
            
            # 獲取請求數據
            request_date = data.get("date")
            begin_time = data.get("begin_time")
            end_time = data.get("end_time")
            time_slice = data.get("time_slice")
            time_slice_unit = data.get("time_slice_unit")
            
            # 驗證數據
            if not all([request_date, begin_time, end_time, time_slice, time_slice_unit]):
                return JsonResponse({
                    "success": False,
                    "message": "缺少必要參數"
                }, status=400)
            
            # 處理時間設置
            with transaction.atomic():
                member = Members.objects.get(id=user_id)
                
                # 生成時間片段
                time_slices = generate_time_slice(
                    begin_time, end_time, time_slice, time_slice_unit, request_date
                )
                
                # 保存時間設置
                time_setting.save_time_period(
                    member.id, request_date, begin_time, end_time, 
                    time_slice, time_slice_unit, time_slices
                )
                
                return JsonResponse({
                    "success": True,
                    "message": "時間設置已保存",
                    "time_slices": time_slices
                })
        
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=400)

# 時間價格 API
@require_http_methods(["GET", "POST"])
@csrf_exempt
@jwt_auth_required
def time_prices_api(request):
    """獲取或設置時間價格"""
    if request.method == "GET":
        try:
            user_id = request.user_id
            member = Members.objects.get(id=user_id)
            
            time_prices = time_pricing.get_time_price(member.id)
            
            return JsonResponse({
                "success": True,
                "time_prices": time_prices
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=400)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = request.user_id
            
            # 獲取請求數據
            request_date = data.get("date")
            time_period_id = data.get("time_period_id")
            price = data.get("price")
            
            # 驗證數據
            if not all([request_date, time_period_id, price]):
                return JsonResponse({
                    "success": False,
                    "message": "缺少必要參數"
                }, status=400)
            
            # 處理時間價格
            with transaction.atomic():
                member = Members.objects.get(id=user_id)
                
                # 保存時間價格
                time_pricing.save_time_price(
                    member.id, request_date, time_period_id, price
                )
                
                return JsonResponse({
                    "success": True,
                    "message": "價格設置已保存"
                })
        
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=400)

# 預約時間 API
@require_http_methods(["GET"])
@csrf_exempt
@jwt_auth_required
def reservation_times_api(request):
    """獲取預約時間"""
    try:
        user_id = request.user_id
        member = Members.objects.get(id=user_id)
        
        # 獲取所有訂單
        orders = Order.objects.filter(merchant_id=member.id)
        appointment_time = []
        
        for order in orders:
            booking = Booking.objects.get(id=order.booking_id)
            
            appointment_time.append({
                "appointmentDate": booking.booking_date,
                "appointmentTime": booking.booking_time,
                "appointmentTotalTime": booking.booking_total_time,
                "consumerName": order.consumer_name
            })
        
        return JsonResponse({
            "success": True,
            "ok": True,  # 兼容原有前端
            "appointment_time": appointment_time
        })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 消費者數據 API
@require_http_methods(["GET"])
@csrf_exempt
@jwt_auth_required
def consumer_data_api(request):
    """獲取消費者數據"""
    try:
        user_id = request.user_id
        member = Members.objects.get(id=user_id)
        
        # 獲取消費者數據
        # 這裡根據實際需求實現
        
        return JsonResponse({
            "success": True,
            "consumer_data": []  # 替換為實際數據
        })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 商家時間段 API
@require_http_methods(["GET"])
@csrf_exempt
@jwt_auth_required
def merchant_time_slots_api(request):
    """獲取商家時間段"""
    try:
        user_id = request.user_id
        member = Members.objects.get(id=user_id)
        
        # 獲取時間段
        time_slots = time_setting.get_all_time_periods(member.id)
        
        return JsonResponse({
            "success": True,
            "time_slots": time_slots
        })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 更新商家時間段 API
@require_http_methods(["POST"])
@csrf_exempt
@jwt_auth_required
def update_merchant_time_slots_api(request):
    """更新商家時間段"""
    try:
        data = json.loads(request.body)
        user_id = request.user_id
        
        # 獲取請求數據
        time_slot_id = data.get("time_slot_id")
        begin_time = data.get("begin_time")
        end_time = data.get("end_time")
        
        # 驗證數據
        if not all([time_slot_id, begin_time, end_time]):
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 更新時間段
        time_setting.update_time_period(time_slot_id, begin_time, end_time)
        
        return JsonResponse({
            "success": True,
            "message": "時間段已更新"
        })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 刪除商家時間段 API
@require_http_methods(["POST"])
@csrf_exempt
@jwt_auth_required
def delete_merchant_time_slots_api(request):
    """刪除商家時間段"""
    try:
        data = json.loads(request.body)
        user_id = request.user_id
        
        # 獲取請求數據
        time_slot_id = data.get("time_slot_id")
        
        # 驗證數據
        if not time_slot_id:
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 刪除時間段
        time_setting.delete_time_period(time_slot_id)
        
        return JsonResponse({
            "success": True,
            "message": "時間段已刪除"
        })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)
