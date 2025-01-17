from django.contrib import admin
from .models import Member, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'choice', 'salat', 'status')
    search_fields = ('member__first_name', 'member__last_name', 'date')
    list_filter = ('status', 'choice')

admin.site.register(Order, OrderAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','id')  # Example fields
    search_fields = ('first_name', 'last_name','id')

admin.site.register(Member, MemberAdmin)

# Register your models here.
