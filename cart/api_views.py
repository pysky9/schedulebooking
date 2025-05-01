import json
import jwt
import os
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction

from members.models import Members
from scheduler.models import Time_setting, Time_pricing
from cart.models import Booking, Cart
from scheduler.api_views import jwt_auth_required

# 預約 API
@require_http_methods(["POST"])
@csrf_exempt
@jwt_auth_required
def booking_api(request):
    """創建預約"""
    try:
        data = json.loads(request.body)
        user_id = request.user_id
        
        # 獲取請求數據
        merchant_id = data.get("merchant_id")
        booking_date = data.get("booking_date")
        booking_time = data.get("booking_time")
        booking_total_time = data.get("booking_total_time")
        booking_price = data.get("booking_price")
        
        # 驗證數據
        if not all([merchant_id, booking_date, booking_time, booking_total_time, booking_price]):
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 創建預約
        with transaction.atomic():
            booking = Booking.objects.create(
                merchant_id=merchant_id,
                booking_date=booking_date,
                booking_time=booking_time,
                booking_total_time=booking_total_time,
                booking_price=booking_price
            )
            
            return JsonResponse({
                "success": True,
                "message": "預約已創建",
                "booking_id": booking.id
            })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 添加到購物車 API
@require_http_methods(["POST"])
@csrf_exempt
@jwt_auth_required
def add_to_cart_api(request):
    """添加項目到購物車"""
    try:
        data = json.loads(request.body)
        user_id = request.user_id
        
        # 獲取請求數據
        booking_id = data.get("booking_id")
        quantity = data.get("quantity", 1)
        
        # 驗證數據
        if not booking_id:
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 添加到購物車
        with transaction.atomic():
            booking = Booking.objects.get(id=booking_id)
            
            # 檢查購物車中是否已有該項目
            cart_item, created = Cart.objects.get_or_create(
                consumer_id=user_id,
                booking_id=booking_id,
                defaults={"quantity": quantity}
            )
            
            # 如果已存在，更新數量
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return JsonResponse({
                "success": True,
                "message": "已添加到購物車",
                "cart_item_id": cart_item.id
            })
    
    except Booking.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "預約不存在"
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 獲取購物車 API
@require_http_methods(["GET"])
@csrf_exempt
@jwt_auth_required
def get_cart_api(request):
    """獲取購物車內容"""
    try:
        user_id = request.user_id
        
        # 獲取購物車項目
        cart_items = Cart.objects.filter(consumer_id=user_id)
        
        # 構建響應數據
        cart_data = []
        total_price = 0
        
        for item in cart_items:
            booking = Booking.objects.get(id=item.booking_id)
            
            # 獲取商家信息
            merchant = Members.objects.get(id=booking.merchant_id)
            
            item_data = {
                "cart_item_id": item.id,
                "booking_id": booking.id,
                "merchant_id": booking.merchant_id,
                "merchant_name": merchant.name,
                "booking_date": booking.booking_date,
                "booking_time": booking.booking_time,
                "booking_total_time": booking.booking_total_time,
                "booking_price": booking.booking_price,
                "quantity": item.quantity,
                "subtotal": item.quantity * booking.booking_price
            }
            
            cart_data.append(item_data)
            total_price += item_data["subtotal"]
        
        return JsonResponse({
            "success": True,
            "cart_items": cart_data,
            "total_price": total_price,
            "item_count": len(cart_data)
        })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 更新購物車項目 API
@require_http_methods(["POST"])
@csrf_exempt
@jwt_auth_required
def update_cart_item_api(request):
    """更新購物車項目數量"""
    try:
        data = json.loads(request.body)
        user_id = request.user_id
        
        # 獲取請求數據
        cart_item_id = data.get("cart_item_id")
        quantity = data.get("quantity")
        
        # 驗證數據
        if not all([cart_item_id, quantity]):
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 更新購物車項目
        with transaction.atomic():
            cart_item = Cart.objects.get(id=cart_item_id, consumer_id=user_id)
            
            if quantity <= 0:
                # 如果數量為0或負數，刪除項目
                cart_item.delete()
                return JsonResponse({
                    "success": True,
                    "message": "購物車項目已刪除"
                })
            else:
                # 更新數量
                cart_item.quantity = quantity
                cart_item.save()
                
                # 計算小計
                booking = Booking.objects.get(id=cart_item.booking_id)
                subtotal = cart_item.quantity * booking.booking_price
                
                return JsonResponse({
                    "success": True,
                    "message": "購物車項目已更新",
                    "quantity": cart_item.quantity,
                    "subtotal": subtotal
                })
    
    except Cart.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "購物車項目不存在"
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 移除購物車項目 API
@require_http_methods(["POST"])
@csrf_exempt
@jwt_auth_required
def remove_cart_item_api(request):
    """從購物車中移除項目"""
    try:
        data = json.loads(request.body)
        user_id = request.user_id
        
        # 獲取請求數據
        cart_item_id = data.get("cart_item_id")
        
        # 驗證數據
        if not cart_item_id:
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 刪除購物車項目
        with transaction.atomic():
            cart_item = Cart.objects.get(id=cart_item_id, consumer_id=user_id)
            cart_item.delete()
            
            return JsonResponse({
                "success": True,
                "message": "購物車項目已刪除"
            })
    
    except Cart.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "購物車項目不存在"
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 清空購物車 API
@require_http_methods(["POST"])
@csrf_exempt
@jwt_auth_required
def clear_cart_api(request):
    """清空購物車"""
    try:
        user_id = request.user_id
        
        # 刪除所有購物車項目
        Cart.objects.filter(consumer_id=user_id).delete()
        
        return JsonResponse({
            "success": True,
            "message": "購物車已清空"
        })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)
