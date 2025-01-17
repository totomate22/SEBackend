from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order.models import Member, Order

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

# Create your views here.