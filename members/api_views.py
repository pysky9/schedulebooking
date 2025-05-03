import json
import jwt
import os
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password

from members.models import Members

# 獲取 JWT 密鑰
jwt_key = os.getenv("jwt_key") or "default_jwt_secret_key"

# 登錄 API
@require_http_methods(["POST"])
@csrf_exempt
def login_api(request):
    """用戶登錄"""
    try:
        data = json.loads(request.body)
        
        # 獲取請求數據
        email = data.get("email")
        password = data.get("password")
        
        # 驗證數據
        if not all([email, password]):
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 驗證用戶
        try:
            member = Members.objects.get(email=email)
            
            # 檢查密碼
            if check_password(password, member.password):
                # 創建 JWT
                payload = {
                    "id": member.id,
                    "email": member.email,
                    "exp": datetime.utcnow() + timedelta(days=7)  # 7天過期
                }
                
                jwt_token = jwt.encode(payload, jwt_key, algorithm="HS256")
                
                # 創建響應
                response = JsonResponse({
                    "success": True,
                    "message": "登錄成功",
                    "user": {
                        "id": member.id,
                        "username": member.username,
                        "email": member.email,
                        "url": member.url
                    }
                })
                
                # 設置 Cookie
                response.set_cookie(
                    "jwt_token",
                    jwt_token,
                    max_age=7 * 24 * 60 * 60,  # 7天
                    httponly=True,
                    samesite="Lax"
                )
                
                return response
            else:
                return JsonResponse({
                    "success": False,
                    "message": "密碼錯誤"
                }, status=401)
        
        except Members.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "用戶不存在"
            }, status=404)
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 註冊 API
@require_http_methods(["POST"])
@csrf_exempt
def register_api(request):
    """用戶註冊"""
    try:
        data = json.loads(request.body)
        
        # 獲取請求數據
        username = data.get("username")  # 前端和後端都使用 username
        email = data.get("email")
        password = data.get("password")
        
        # 生成 URL（可以是用戶名或電子郵件的一部分）
        url = f"/scheduler/views/{data['username']}"
        
        # 驗證數據
        if not all([username, email, password]):
            return JsonResponse({
                "success": False,
                "message": "缺少必要參數"
            }, status=400)
        
        # 檢查郵箱是否已存在
        if Members.objects.filter(email=email).exists():
            return JsonResponse({
                "success": False,
                "message": "郵箱已被註冊"
            }, status=400)
        
        # 創建用戶
        with transaction.atomic():
            member = Members.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                url=url
            )
            
            # 創建 JWT
            payload = {
                "id": member.id,
                "email": member.email,
                "exp": datetime.utcnow() + timedelta(days=7)  # 7天過期
            }
            
            jwt_token = jwt.encode(payload, jwt_key, algorithm="HS256")
            
            # 創建響應
            response = JsonResponse({
                "success": True,
                "message": "註冊成功",
                "user": {
                    "id": member.id,
                    "username": member.username,
                    "email": member.email,
                    "url": member.url
                }
            })
            
            # 設置 Cookie
            response.set_cookie(
                "jwt_token",
                jwt_token,
                max_age=7 * 24 * 60 * 60,  # 7天
                httponly=True,
                samesite="Lax"
            )
            
            return response
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 登出 API
@require_http_methods(["POST"])
@csrf_exempt
def logout_api(request):
    """用戶登出"""
    try:
        # 創建響應
        response = JsonResponse({
            "success": True,
            "message": "登出成功"
        })
        
        # 刪除 Cookie
        response.delete_cookie("jwt_token")
        
        return response
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 獲取用戶資料 API
@require_http_methods(["GET"])
@csrf_exempt
def profile_api(request):
    """獲取用戶資料"""
    try:
        # 獲取 JWT
        jwt_token = request.COOKIES.get("jwt_token") or request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not jwt_token:
            return JsonResponse({
                "success": False,
                "message": "未授權訪問，請先登錄"
            }, status=401)
        
        # 解析 JWT
        try:
            payload = jwt.decode(jwt_token, jwt_key, algorithms=["HS256"])
            user_id = payload.get("id")
            
            # 獲取用戶資料
            member = Members.objects.get(id=user_id)
            
            return JsonResponse({
                "success": True,
                "user": {
                    "id": member.id,
                    "username": member.username,
                    "email": member.email,
                    "url": member.url
                }
            })
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                "success": False,
                "message": "登錄已過期，請重新登錄"
            }, status=401)
        
        except jwt.InvalidTokenError:
            return JsonResponse({
                "success": False,
                "message": "無效的登錄憑證"
            }, status=401)
        
        except Members.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "用戶不存在"
            }, status=404)
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 更新用戶資料 API
@require_http_methods(["POST"])
@csrf_exempt
def update_profile_api(request):
    """更新用戶資料"""
    try:
        # 獲取 JWT
        jwt_token = request.COOKIES.get("jwt_token") or request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not jwt_token:
            return JsonResponse({
                "success": False,
                "message": "未授權訪問，請先登錄"
            }, status=401)
        
        # 解析 JWT
        try:
            payload = jwt.decode(jwt_token, jwt_key, algorithms=["HS256"])
            user_id = payload.get("id")
            
            # 獲取請求數據
            data = json.loads(request.body)
            username = data.get("username")  # 前端和後端都使用 username
            
            # 驗證數據
            if not username:
                return JsonResponse({
                    "success": False,
                    "message": "缺少必要參數"
                }, status=400)
            
            # 更新用戶資料
            with transaction.atomic():
                member = Members.objects.get(id=user_id)
                member.username = username
                member.save()
                
                return JsonResponse({
                    "success": True,
                    "message": "資料已更新",
                    "user": {
                        "id": member.id,
                        "username": member.username,
                        "email": member.email,
                        "url": member.url
                    }
                })
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                "success": False,
                "message": "登錄已過期，請重新登錄"
            }, status=401)
        
        except jwt.InvalidTokenError:
            return JsonResponse({
                "success": False,
                "message": "無效的登錄憑證"
            }, status=401)
        
        except Members.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "用戶不存在"
            }, status=404)
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 修改密碼 API
@require_http_methods(["POST"])
@csrf_exempt
def change_password_api(request):
    """修改密碼"""
    try:
        # 獲取 JWT
        jwt_token = request.COOKIES.get("jwt_token") or request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not jwt_token:
            return JsonResponse({
                "success": False,
                "message": "未授權訪問，請先登錄"
            }, status=401)
        
        # 解析 JWT
        try:
            payload = jwt.decode(jwt_token, jwt_key, algorithms=["HS256"])
            user_id = payload.get("id")
            
            # 獲取請求數據
            data = json.loads(request.body)
            old_password = data.get("old_password")
            new_password = data.get("new_password")
            
            # 驗證數據
            if not all([old_password, new_password]):
                return JsonResponse({
                    "success": False,
                    "message": "缺少必要參數"
                }, status=400)
            
            # 修改密碼
            with transaction.atomic():
                member = Members.objects.get(id=user_id)
                
                # 檢查舊密碼
                if not check_password(old_password, member.password):
                    return JsonResponse({
                        "success": False,
                        "message": "舊密碼錯誤"
                    }, status=401)
                
                # 更新密碼
                member.password = make_password(new_password)
                member.save()
                
                return JsonResponse({
                    "success": True,
                    "message": "密碼已修改"
                })
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                "success": False,
                "message": "登錄已過期，請重新登錄"
            }, status=401)
        
        except jwt.InvalidTokenError:
            return JsonResponse({
                "success": False,
                "message": "無效的登錄憑證"
            }, status=401)
        
        except Members.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "用戶不存在"
            }, status=404)
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

# 檢查認證狀態 API
@require_http_methods(["GET"])
@csrf_exempt
def check_auth_api(request):
    """檢查認證狀態"""
    try:
        # 獲取 JWT
        jwt_token = request.COOKIES.get("jwt_token") or request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not jwt_token:
            return JsonResponse({
                "success": False,
                "authenticated": False,
                "message": "未登錄"
            })
        
        # 解析 JWT
        try:
            payload = jwt.decode(jwt_token, jwt_key, algorithms=["HS256"])
            user_id = payload.get("id")
            
            # 獲取用戶資料
            member = Members.objects.get(id=user_id)
            
            return JsonResponse({
                "success": True,
                "authenticated": True,
                "user": {
                    "id": member.id,
                    "name": member.username,  # 返回前端期望的 name 欄位
                    "email": member.email,
                    "url": member.url
                }
            })
        
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Members.DoesNotExist):
            return JsonResponse({
                "success": False,
                "authenticated": False,
                "message": "認證失敗"
            })
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "authenticated": False,
            "message": str(e)
        })
