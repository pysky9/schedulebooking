import os
import json
import jwt
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

from dotenv import load_dotenv

from membersApp.models import Members
from lineApp.models import Customers
from cartApp.models import Booking
from orderApp.models import Order

load_dotenv() 

jwt_key = os.getenv("jwt_key")

def login_signup(request):
    return render(request, "loginSignup.html")

def member_page(request, username):
    name = username
    return render(request, "members.html", locals())

def site_map(request, username):
    return render(request, "sitemap.html")

def customer_management(request, storename):
    return render(request, "customermanagement.html")

def store_setting(request, storename):
    name = storename
    return render(request, "stroesetting.html", locals())

def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if Members.objects.filter(username=data["username"]):
            return JsonResponse({"ok": False, "msg": "username已被註冊"})
        if Members.objects.filter(email=data["email"]):
            return JsonResponse({"ok": False, "msg": "email已被註冊"})
        try:
            members = Members()
            members.username = data["username"]
            members.email = data["email"]
            members.password = make_password(data["password"])
            members.url = f"/calendar/views/{data['username']}"
            members.save()
        except:
            return JsonResponse({"ok": False, "msg": "Server got wrong"})
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False, "msg": "HTTP Method got wrong"})
 
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data["email"]
        password = data["password"]
        query = Members.objects.filter(email=email)
        if not query:
            return JsonResponse({"ok": False, "msg": "Email 錯誤"})
        db_password = query[0].password
        is_valid_password = check_password(password, db_password)
        if is_valid_password:
            id = query[0].id
            username = query[0].username
            expiration_time = datetime.utcnow() + timedelta(weeks=1)
            payload = {
                "id": f"{id}",
                "username": f"{username}",
                "email": f"{email}",
                "exp": expiration_time
            }
            jwt_encode = jwt.encode(payload, jwt_key, algorithm = "HS256")
            response = JsonResponse({"ok": True, "username": username})
            response.set_cookie(key="jwt_token", value=jwt_encode, expires=expiration_time)
            return response
        
        return JsonResponse({"ok": False, "msg": "Password 錯誤"})
    return JsonResponse({"ok": False, "msg": "HTTP Method got wrong"})

def logout(request):
    response = JsonResponse({"ok": True})
    response.set_cookie(key="jwt_token", value="", expires=0)
    return response

def get_members_info(request):
    get_cookie = request.COOKIES.get("jwt_token")
    try:
        payloads = jwt.decode(get_cookie, jwt_key, algorithms = "HS256")
        query = Members.objects.filter(email=payloads["email"])
        db_url = query[0].url
        data = {
            "id": payloads["id"],
            "username": payloads["username"],
            "email": payloads["email"],
            "url": db_url
        }
        return JsonResponse({"data": data})
    except:
        return JsonResponse({"data": None})


