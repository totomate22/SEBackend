from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order.models import Member, Order
from users.models import User

from datetime import datetime



def homepage(request):
    return render(request, 'homepage.html', {})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'gruppenleitung':
                return redirect('group_dashboard') 
            if user.role == 'standortleitung':
                return redirect('standortleitung_dashboard') 
            return redirect('home')  # Redirect to home page or dashboard
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def home_view(request):
    return render(request, 'home.html')

# Group-Dashboard and Functions

@login_required
def group_dashboard(request):
    user = request.user
    user_group_id = user.group_id

    members =  Member.objects.filter(group_id=user_group_id)
    orders = Order.objects.filter(member__group_id=user_group_id)


    return render(request, 'group_dashboard.html', {
        'user': user,
        'members': members,
        'orders': orders,
    })

def add_order(request):
    if request.method == 'POST':
        member_id = request.POST.get('member')
        choice = request.POST.get('choice')
        salat = 'salat' in request.POST
        date = request.POST.get('date')
        
        member = Member.objects.get(id=member_id)
        order = Order(member=member, choice=choice, salat=salat, date=date)
        order.save()

        messages.success(request, "Order added successfully.")
        return redirect('group_dashboard')
    return render(request, 'group_dashboard.html')

@login_required
def delete_orders(request):
    if request.method == 'POST':
        # Get the list of order IDs to delete from the form
        orders_to_delete = request.POST.getlist('orders_to_delete')

        # Filter and delete the orders
        Order.objects.filter(id__in=orders_to_delete).delete()

        # Redirect back to the dashboard
        return redirect('group_dashboard')  # Replace 'group_dashboard' with the name of your dashboard URL
    else:
        # Redirect to dashboard if accessed via GET
        return redirect('group_dashboard')
    
# Standortleitung-Dashboard and Function

@login_required
def standortleitung_dashboard(request):
    user = request.user
    user_location = user.location

    members =  Member.objects.filter(location=user_location)
    orders = Order.objects.filter(member__location=user_location)
    users = User.objects.filter(location=user_location,role='gruppenleitung')       #nochmal nachfragen, ob auch sl mit reins soll


    return render(request, 'standortleitung_dashboard.html', {
        'user': user,
        'members': members,
        'orders': orders,
        'users': users,
    })

@login_required
def add_member(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        group_id =request.POST.get('group_id')
        location=request.POST.get('location')
        
        member = Member(first_name=first_name, last_name=last_name, group_id=group_id,location=location)
        member.save()
        messages.success(request, "Order added successfully.")
        return redirect('standortleitung_dashboard')
    return render(request, 'standortleitung_dashboard.html')

@login_required
def delete_members(request):
    if request.method == 'POST':
        # Get the list of order IDs to delete from the form
        members_to_delete = request.POST.getlist('members_to_delete')

        # Filter and delete the orders
        Order.objects.filter(id__in=members_to_delete).delete()

        # Redirect back to the dashboard
        return redirect('standortleitung_dashboard')  # Replace 'group_dashboard' with the name of your dashboard URL
    else:
        # Redirect to dashboard if accessed via GET
        return redirect('standortleitung_dashboard')

# Create your views here.