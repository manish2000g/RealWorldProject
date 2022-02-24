from django.shortcuts import render, redirect
from .forms import Activity_Type_Form, Activity_Form, Order_Form
from django.contrib import messages
from .models import Activity_Type, Activity, Cart, Order
from accounts.auth import admin_only, user_only
from django.contrib.auth.decorators import login_required
import os
from django.core.mail import send_mail
from django.conf import settings


@login_required
@admin_only
def activity_type_form(request):
    if request.method == "POST":
        form = Activity_Type_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Activity Type added")
            return redirect("/resort/get_activity_type")
        else:
            messages.add_message(request, messages.ERROR, "Unable to add activity type")
            return render(request, 'resort/activity_type_form.html', {'activity_type_form': form})
    context = {
        'activity_type_form': Activity_Type_Form,
        'activate_activity_type': 'active'
    }
    return render(request, 'resort/activity_type_form.html', context)


@login_required
@admin_only
def get_activity_type(request):
    activity_types = Activity_Type.objects.all().order_by('-id')
    context = {
        'activity_types': activity_types,
        'activate_activity_type': 'active'
    }
    return render(request, 'resort/get_activity_type.html', context)


@login_required
@admin_only
def delete_activity_type(request, activity_type_id):
    activity_type = Activity_Type.objects.get(id=activity_type_id)
    os.remove(activity_type.activity_type_img.path)
    activity_type.delete()
    messages.add_message(request, messages.SUCCESS, "Activity type deleted")
    return redirect('/resort/get_activity_type')


@login_required
@admin_only
def update_activity_type(request, activity_type_id):
    activity_type = Activity_Type.objects.get(id=activity_type_id)
    if request.method == "POST":
        if request.FILES.get('activity_type_img'):
            os.remove(activity_type.activity_img.path)
        form = Activity_Type_Form(request.POST, instance=activity_type)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Activity Type updated successfully')
            return redirect("/resort/get_activity_type")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to update activity type')
            return render(request, 'resort/activity_type_update_form.html', {'form_activity_type': form})
    context = {
        'form_activity_type': Activity_Type_Form(instance=activity_type),
        'activate_activity_type': 'active'
    }
    return render(request, 'resort/activity_type_update_form.html', context)


@login_required
@admin_only
def activity_form(request):
    if request.method == "POST":
        form = Activity_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Activity added succesfully")
            return redirect("/resort/get_activity")
        else:
            messages.add_message(request, messages.ERROR, "Unable to add activity ")
            return render(request, 'resort/activity_form.html', {'activity_form': form})
    context = {
        'activity_form': Activity_Form,
        'activate_activity': 'active'
    }
    return render(request, 'resort/activity_form.html', context)


@login_required
@admin_only
def get_activity(request):
    activities = Activity.objects.all().order_by('-id')
    context = {
        'activities': activities,
        'activate_activity': 'active'
    }
    return render(request, 'resort/get_activity.html', context)


@login_required
@admin_only
def delete_activity(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    os.remove(activity.activity_img.path)
    activity.delete()
    messages.add_message(request, messages.SUCCESS, 'Activity deleted')
    return redirect('/resort/get_activity')


@login_required
@admin_only
def update_activity(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    if request.method == "POST":
        if request.FILES.get('activity_img'):
            os.remove(activity.activity_img.path)
        form = Activity_Form(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Activity updated successfully')
            return redirect("/resort/get_activity")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to update activity')
            return render(request, 'resort/activity_form.html', {'form_activity': form})
    context = {
        'activity_form': Activity_Form(instance=activity),
        'activate_activity': 'active'
    }
    return render(request, 'resort/activity_update_form.html', context)


def view_activities(request):
    print("1")
    if 'q' in request.GET:
        q = request.GET['q']
        print("here")
        activities = Activity.objects.filter(activity_name__icontains=q)
    else:
        activities = Activity.objects.all().order_by('-id')
    context = {
        'activities': activities,
        'activate_user_activity': 'active'
    }
    return render(request, 'resort/activities_view.html', context)


@login_required
@user_only
def add_to_cart(request, activity_id):
    user = request.user
    activity = Activity.objects.get(id=activity_id)

    cart_item = Cart.objects.filter(user=user, activity=activity)
    if cart_item:
        messages.add_message(request, messages.ERROR, 'Activity has already been added to the cart')
        return redirect('/resort/activities_view')
    else:
        cart = Cart.objects.create(activity=activity, user=user)
        if cart:
            messages.add_message(request, messages.SUCCESS, 'Activity added to the cart')
            return redirect('/resort/user_cart')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add activity to the cart')


@login_required
@user_only
def view_cart_activities(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {
        'items': items,
        'activate_user_cart': 'active'
    }
    return render(request, 'resort/user_cart.html', context)


@login_required
@user_only
def delete_cart_activity(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    messages.add_message(request, messages.SUCCESS, 'Activity removed successfully')
    return redirect('/resort/user_cart')


@login_required
@user_only
def order_form(request, activity_id, cart_id):
    user = request.user
    activity = Activity.objects.get(id=activity_id)
    cart_item = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        form = Order_Form(request.POST)
        if form.is_valid():
            quantity = request.POST.get('quantity')
            price = activity.activity_price
            price = int(quantity) * int(price)
            contact_no = request.POST.get('contact_no')
            user_address = request.POST.get('user_address')
            payment_method = request.POST.get('payment_method')
            order = Order.objects.create(activity=activity,
                                         user=user,
                                         quantity=quantity,
                                         price=price,
                                         contact_no=contact_no,
                                         user_address=user_address,
                                         status="Pending",
                                         payment_method=payment_method,
                                         payment_status=False
                                         )
            if order:
                context = {
                    'order': order,
                    'cart': cart_item
                }
                return render(request, 'resort/esewa_payment.html', context)
            else:
                messages.add_message(request, messages.ERROR, 'Something went wrong')
                return render(request, 'activities/order_form.html', {'order_form': form})
    context = {
        'order_form': Order_Form
    }
    return render(request, 'resort/order_form.html', context)


# import requests as req
def esewa_verify(request):
    import xml.etree.ElementTree as ET
    o_id = request.GET.get('oid')
    amount = request.GET.get('amt')
    refId = request.GET.get('refId')
    url = "https://uat.esewa.com.np/epay/transrec"
    d = {
        'amt': amount,
        'scd': 'EPAYTEST',
        'rid': refId,
        'pid': o_id,
    }
    resp = request.post(url, d)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()
    if status == 'Success':
        order_id = o_id.split("_")[0]
        order = Order.objects.get(id=order_id)
        order.payment_status = True
        order.save()
        cart_id = o_id.split("_")[1]
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        messages.add_message(request, messages.SUCCESS, 'Payment Successful')
        return redirect('/resort/user_cart')
    else:
        messages.add_message(request, messages.ERROR, 'Unable to make payment')
        return redirect('/resort/user_cart')


@login_required
@user_only
def user_order(request):
    user = request.user
    items = Order.objects.filter(user=user).order_by('-id')
    context = {
        'items': items,
        'activate_user_orders': 'active'
    }
    return render(request, 'resort/user_order.html', context)


def home(request):
    activity_types = Activity_Type.objects.all().order_by('-id')
    if request.method == "POST":
        subject = request.POST.get("subject")
        email = request.POST.get("email")
        desc = request.POST.get("desc") + "\n" + "Send to: "+email
        send_mail(subject, desc, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
    context = {
        'activity_types': activity_types,
    }
    return render(request, 'resort/home.html', context)
