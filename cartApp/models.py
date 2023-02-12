from django.db import models
from membersApp.models import Members

# Create your models here.
class Booking(models.Model):
    members_id = models.ForeignKey(Members, on_delete=models.CASCADE, related_name="booking")
    booking_id = models.CharField(max_length=150)
    booking_date = models.CharField(max_length=150, null=False)
    booking_time = models.CharField(max_length=50, null=False)
    booking_total_time = models.CharField(max_length=50, null=False)
    booking_price = models.CharField(max_length=50, null=False)
    booking_status = models.CharField(max_length=15)