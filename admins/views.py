from django.shortcuts import render
from django.contrib.auth.models import User
from resort import models

def admin_dashboard(request):
    orders = models.Order.objects.count()
    users = User.objects.all()
    list = []
    user_count = users.filter(is_staff=0).count()
    admin_count = users.filter(is_staff=1).count()
    items = orders
    context = {
        'user': user_count,
        'admin': admin_count,
        'items': items

    }
    return render(request, 'admins/admin_dashboard.html', context)