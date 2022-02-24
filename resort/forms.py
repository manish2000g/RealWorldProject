from django import forms
from django.forms import ModelForm
from .models import Activity_Type,Activity,Order

class Activity_Type_Form(ModelForm):
    class Meta:
        model= Activity_Type
        fields="__all__"


class Activity_Form(ModelForm):
    class Meta:
        model= Activity
        fields= "__all__"

class Order_Form(ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'contact_no', 'user_address','payment_method']