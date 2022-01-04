from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator
from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.core import validators


class Activity_Type(models.Model):
    activity_Type_name=models.CharField(max_length=200,null=True,validators=[validators.MinLengthValidator(2)])
    activity_Type_description=models.TextField(null=True)
    activity_Type_img=models.FileField(upload_to='static/uploads')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
         return self.activity_Type_name


class Activity(models.Model):
    activity_name=models.CharField(max_length=100)
    activity_price=models.FloatField()
    activity_img=models.FileField(upload_to='static/uploads')
    activity_Type = models.ForeignKey(Activity_Type, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.activity_name
    
    
class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )
    PAYMENT = (
        ('Cash On Delivery', 'Cash On Delivery'),
        ('Esewa', 'Esewa'),
        ('Khalti', 'Khalti'),
    )
    activity = models.ForeignKey(Activity, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    price = models.IntegerField(null=True)
    payment_method = models.CharField(max_length=200, choices=PAYMENT, null=True)
    payment_status = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=200, choices=STATUS, null=True)
    contact_no = models.CharField(validators=[MinLengthValidator(9), MaxLengthValidator(10)], null=True, max_length=10)
    user_address = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
