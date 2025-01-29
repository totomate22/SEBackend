from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order.models import Member, Order
from users.models import User
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from datetime import datetime

import csv
from django.http import HttpResponse


# General Methods

def delete_items(model, ids):
    model.objects.filter(id__in=ids).delete()

#
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
            if user.role == 'verwaltung':
                return redirect('verwaltung_dashboard')
            return redirect('home')  # Redirect to home page or dashboard
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
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
        delete_items(Order, orders_to_delete)
        # Redirect back to the dashboard
        return redirect('group_dashboard') 
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
        messages.success(request, "Member added successfully.")
        return redirect('standortleitung_dashboard')
    return render(request, 'standortleitung_dashboard.html')

@login_required
def delete_members(request):
    if request.method == 'POST':
        # Get the list of order IDs to delete from the form
        members_to_delete = request.POST.getlist('members_to_delete')
        delete_items(Order, members_to_delete)

        # Redirect back to the dashboard
        return redirect('standortleitung_dashboard')  
    else:
        # Redirect to dashboard if accessed via GET
        return redirect('standortleitung_dashboard')
    
#Verwaltung-Dashboard und Funktionen

@login_required
def verwaltung_dashboard(request):
    if request.user.role != 'verwaltung':  # Restrict access
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    selected_location = request.GET.get('location', 'all')  # Default to "all"
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')

    # Fetch locations from users and members
    user_locations = User.objects.exclude(location__isnull=True).values_list('location', flat=True).distinct()
    member_locations = Member.objects.exclude(location__isnull=True).values_list('location', flat=True).distinct()
    locations = ["1", "2", "3"]

    members = Member.objects.all()
    gruppenleitung_users = User.objects.filter(role='gruppenleitung')
    standortleitung_users = User.objects.filter(role='standortleitung')

    if selected_location in locations:
        members = members.filter(location=selected_location)
        gruppenleitung_users = gruppenleitung_users.filter(location=selected_location)
        standortleitung_users = standortleitung_users.filter(location=selected_location)
    if search_query:
        members = members.filter(first_name__icontains=search_query) | members.filter(last_name__icontains=search_query)
        gruppenleitung_users = gruppenleitung_users.filter(first_name__icontains=search_query) | gruppenleitung_users.filter(last_name__icontains=search_query)
        standortleitung_users = standortleitung_users.filter(first_name__icontains=search_query) | standortleitung_users.filter(last_name__icontains=search_query)
    
    if role_filter:
        if role_filter == "gruppenleitung":
            standortleitung_users = []
            members = []  # Hide members
        elif role_filter == "standortleitung":
            gruppenleitung_users = []
            members = []  # Hide members


    if "export_csv" in request.GET:
        return export_csv(members)

    return render(request, 'verwaltung_dashboard.html', {
        'locations': ["all"] + locations,
        'selected_location': selected_location,
        'search_query': search_query,
        'role_filter': role_filter,
        'members': members,
        'gruppenleitung_users': gruppenleitung_users,
        'standortleitung_users': standortleitung_users,
    })


def export_csv(members, gruppenleitung_users, standortleitung_users):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_members.csv"'
    writer = csv.writer(response)
    
    # Header
    writer.writerow(["Type", "First Name", "Last Name", "Username", "Role", "Location", "Group ID"])
    
    # Write data
    for user in gruppenleitung_users:
        writer.writerow(["Gruppenleitung", user.first_name, user.last_name, user.username, user.role, user.location, "-"])
    
    for user in standortleitung_users:
        writer.writerow(["Standortleitung", user.first_name, user.last_name, user.username, user.role, user.location, "-"])
    
    for member in members:
        writer.writerow(["Member", member.first_name, member.last_name, "-", "-", member.location, member.group_id])

    return response


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('verwaltung_dashboard')


@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    messages.success(request, "Member deleted successfully.")
    return redirect('verwaltung_dashboard')

login_required
def create_staff(request):
    if request.user.role != 'verwaltung':  # Restrict access
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        location = request.POST.get('location')
        password = request.POST.get('password')

        # Generate username from first & last name
        username = slugify(f"{first_name}.{last_name}")

        # Ensure role is valid
        if role not in ['gruppenleitung', 'standortleitung']:
            messages.error(request, "Invalid role selected.")
            return redirect('create_staff')

        # Create new user
        new_user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            role=role,
            location=location,
            password=make_password(password)  # Hash password for security
        )

        messages.success(request, f"New {role} user '{username}' created successfully!")
        return redirect('verwaltung_dashboard')

    return render(request, 'create_staff.html')
# Create your views here.