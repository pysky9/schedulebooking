from django.db import models
from members.models import Members
from line_service.models import Customers

# Create your models here.
class Booking(models.Model):
    merchant_id = models.IntegerField(null=False)  # 商家 ID
    booking_date = models.CharField(max_length=150, null=False)  # 預約日期
    booking_time = models.CharField(max_length=50, null=False)  # 預約時間
    booking_total_time = models.CharField(max_length=50, null=False)  # 總時長
    booking_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)  # 價格
    booking_status = models.CharField(max_length=100, default='pending')  # 預約狀態
    created_at = models.DateTimeField(auto_now_add=True)  # 創建時間
    updated_at = models.DateTimeField(auto_now=True)  # 更新時間

    def __str__(self):
        return f"Booking {self.id} - {self.booking_date} {self.booking_time}"

class Cart(models.Model):
    consumer_id = models.IntegerField(null=False)  # 消費者 ID
    booking_id = models.IntegerField(null=False)  # 預約 ID
    quantity = models.IntegerField(default=1)  # 數量
    created_at = models.DateTimeField(auto_now_add=True)  # 創建時間
    updated_at = models.DateTimeField(auto_now=True)  # 更新時間

    def __str__(self):
        return f"Cart {self.id} - Consumer {self.consumer_id}, Booking {self.booking_id}"
