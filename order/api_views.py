import json
import jwt
import os
from datetime import datetime
import uuid

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction

from members.models import Members
from cart.models import Booking, Cart
from order.models import Order, OrderItem
from scheduler.api_views import jwt_auth_required

# 創建訂單 API
@require_http_methods(["POST"])
@csrf_exempt
@jwt_auth_required
def create_order_api(request):
    """創建訂單"""
    try:
        data = json.loads(request.body)
        user_id = request.user_id
        
        # 獲取請求數據
        cart_item_ids = data.get("cart_item_ids", [])
        consumer_name = data.get("consumer_name")
        consumer_email = data.get("consumer_email")
        consumer_phone = data.get("consumer_phone")
        payment_method = data.get("payment_method")
        
        # 驗證數據
        if not all([cart_item_ids, consumer_name, consumer_email, consumer_phone, payment_method]):
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 創建訂單
        with transaction.atomic():
            # 獲取購物車項目
            cart_items = Cart.objects.filter(id__in=cart_item_ids, consumer_id=user_id)
            
            if not cart_items:
                return JsonResponse({
                    "success": False,
                    "message": "購物車為空或項目不存在"
                }, status=400)
            
            # 計算總價
            total_price = 0
            order_items_data = []
            
            for cart_item in cart_items:
                booking = Booking.objects.get(id=cart_item.booking_id)
                subtotal = float(booking.booking_price) * cart_item.quantity
                total_price += subtotal
                
                order_items_data.append({
                    "booking_id": booking.id,
                    "merchant_id": booking.merchant_id,
                    "quantity": cart_item.quantity,
                    "price": booking.booking_price,
                    "subtotal": subtotal
                })
            
            # 創建訂單
            order = Order.objects.create(
                order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                consumer_id=user_id,
                consumer_name=consumer_name,
                consumer_email=consumer_email,
                consumer_phone=consumer_phone,
                total_price=total_price,
                payment_method=payment_method,
                status="pending"
            )
            
            # 創建訂單項目
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    booking_id=item_data["booking_id"],
                    merchant_id=item_data["merchant_id"],
                    quantity=item_data["quantity"],
                    price=item_data["price"],
                    subtotal=item_data["subtotal"]
                )
            
            # 清空購物車
            cart_items.delete()
            
            return JsonResponse({
                "success": True,
                "message": "訂單已創建",
                "order_id": order.id,
                "order_number": order.order_number
            })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 獲取訂單列表 API
@require_http_methods(["GET"])
@csrf_exempt
@jwt_auth_required
def get_orders_api(request):
    """獲取訂單列表"""
    try:
        user_id = request.user_id
        user_role = request.GET.get("role", "consumer")  # 默認為消費者角色
        
        if user_role == "merchant":
            # 商家查看自己的訂單
            order_items = OrderItem.objects.filter(merchant_id=user_id)
            order_ids = order_items.values_list('order_id', flat=True).distinct()
            orders = Order.objects.filter(id__in=order_ids)
        else:
            # 消費者查看自己的訂單
            orders = Order.objects.filter(consumer_id=user_id)
        
        # 構建響應數據
        orders_data = []
        
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            items_data = []
            
            for item in order_items:
                booking = Booking.objects.get(id=item.booking_id)
                merchant = Members.objects.get(id=item.merchant_id)
                
                items_data.append({
                    "item_id": item.id,
                    "booking_id": item.booking_id,
                    "merchant_id": item.merchant_id,
                    "merchant_name": merchant.name,
                    "booking_date": booking.booking_date,
                    "booking_time": booking.booking_time,
                    "booking_total_time": booking.booking_total_time,
                    "quantity": item.quantity,
                    "price": float(item.price),
                    "subtotal": float(item.subtotal)
                })
            
            orders_data.append({
                "order_id": order.id,
                "order_number": order.order_number,
                "consumer_name": order.consumer_name,
                "consumer_email": order.consumer_email,
                "consumer_phone": order.consumer_phone,
                "total_price": float(order.total_price),
                "payment_method": order.payment_method,
                "status": order.status,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "items": items_data
            })
        
        return JsonResponse({
            "success": True,
            "orders": orders_data
        })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 獲取訂單詳情 API
@require_http_methods(["GET"])
@csrf_exempt
@jwt_auth_required
def get_order_details_api(request, order_id):
    """獲取訂單詳情"""
    try:
        user_id = request.user_id
        
        # 獲取訂單
        try:
            order = Order.objects.get(id=order_id)
            
            # 檢查權限
            if order.consumer_id != user_id:
                # 檢查是否為商家
                order_items = OrderItem.objects.filter(order=order, merchant_id=user_id)
                if not order_items.exists():
                    return JsonResponse({
                        "success": False,
                        "message": "無權訪問該訂單"
                    }, status=403)
            
            # 獲取訂單項目
            order_items = OrderItem.objects.filter(order=order)
            items_data = []
            
            for item in order_items:
                booking = Booking.objects.get(id=item.booking_id)
                merchant = Members.objects.get(id=item.merchant_id)
                
                items_data.append({
                    "item_id": item.id,
                    "booking_id": item.booking_id,
                    "merchant_id": item.merchant_id,
                    "merchant_name": merchant.name,
                    "booking_date": booking.booking_date,
                    "booking_time": booking.booking_time,
                    "booking_total_time": booking.booking_total_time,
                    "quantity": item.quantity,
                    "price": float(item.price),
                    "subtotal": float(item.subtotal)
                })
            
            # 構建響應數據
            order_data = {
                "order_id": order.id,
                "order_number": order.order_number,
                "consumer_name": order.consumer_name,
                "consumer_email": order.consumer_email,
                "consumer_phone": order.consumer_phone,
                "total_price": float(order.total_price),
                "payment_method": order.payment_method,
                "status": order.status,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "items": items_data
            }
            
            return JsonResponse({
                "success": True,
                "order": order_data
            })
        
        except Order.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "訂單不存在"
            }, status=404)
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 更新訂單狀態 API
@require_http_methods(["POST"])
@csrf_exempt
@jwt_auth_required
def update_order_status_api(request):
    """更新訂單狀態"""
    try:
        data = json.loads(request.body)
        user_id = request.user_id
        
        # 獲取請求數據
        order_id = data.get("order_id")
        status = data.get("status")
        
        # 驗證數據
        if not all([order_id, status]):
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 檢查狀態是否有效
        valid_statuses = ["pending", "paid", "processing", "completed", "cancelled"]
        if status not in valid_statuses:
            return JsonResponse({
                "success": False,
                "message": "無效的訂單狀態"
            }, status=400)
        
        # 更新訂單狀態
        with transaction.atomic():
            try:
                order = Order.objects.get(id=order_id)
                
                # 檢查權限
                if order.consumer_id != user_id:
                    # 檢查是否為商家
                    order_items = OrderItem.objects.filter(order=order, merchant_id=user_id)
                    if not order_items.exists():
                        return JsonResponse({
                            "success": False,
                            "message": "無權更新該訂單"
                        }, status=403)
                
                # 更新狀態
                order.status = status
                order.save()
                
                return JsonResponse({
                    "success": True,
                    "message": "訂單狀態已更新",
                    "status": status
                })
            
            except Order.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "message": "訂單不存在"
                }, status=404)
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 取消訂單 API
@require_http_methods(["POST"])
@csrf_exempt
@jwt_auth_required
def cancel_order_api(request):
    """取消訂單"""
    try:
        data = json.loads(request.body)
        user_id = request.user_id
        
        # 獲取請求數據
        order_id = data.get("order_id")
        
        # 驗證數據
        if not order_id:
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 取消訂單
        with transaction.atomic():
            try:
                order = Order.objects.get(id=order_id)
                
                # 檢查權限
                if order.consumer_id != user_id:
                    return JsonResponse({
                        "success": False,
                        "message": "無權取消該訂單"
                    }, status=403)
                
                # 檢查訂單狀態
                if order.status == "completed":
                    return JsonResponse({
                        "success": False,
                        "message": "已完成的訂單無法取消"
                    }, status=400)
                
                # 更新狀態
                order.status = "cancelled"
                order.save()
                
                return JsonResponse({
                    "success": True,
                    "message": "訂單已取消"
                })
            
            except Order.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "message": "訂單不存在"
                }, status=404)
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)
