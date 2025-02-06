"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'), #homepage
    path('favicon.ico', views.favicon_view),
    path('login/',views.login_view, name='login'),  # Global loginpage
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),    #home after login
    path('group_dashboard/', views.group_dashboard, name='group_dashboard'),    #gruppenansicht
    path('group_dashboard_kitchen/', views.group_dashboard_kitchen, name='group_dashboard_kitchen'),    #gruppenansicht
    path('add_order/', views.add_order, name='add_order'),      #order hinzufügen
    path('delete-orders/', views.delete_orders, name='delete_orders'),  #order löschen
    path('standortleitung_dashboard/', views.standortleitung_dashboard, name='standortleitung_dashboard'),  #standortleitungansicht
    path('add_member/', views.add_member, name='add_member'), #member hinzufügen
    path('delete-members/', views.delete_members, name='delete_members'),   #members löschen
    path('verwaltung_dashboard/', views.verwaltung_dashboard, name='verwaltung_dashboard'), #verwaltungsdashboard
    path('create_staff/', views.create_staff, name='create_staff'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('mark_orders_as_delivered/<int:member_id>/', views.mark_orders_as_delivered, name='mark_orders_as_delivered'),
    path('qr_scanner/', views.qr_scanner, name='qr_scanner'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   #verweist auf settings für qr-code
