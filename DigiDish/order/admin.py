from django.contrib import admin
from django.utils.html import format_html
from .models import Member, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'choice', 'salat', 'status')
    search_fields = ('member__first_name', 'member__last_name', 'date')
    list_filter = ('status', 'choice')

admin.site.register(Order, OrderAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'id')  # Example fields
    search_fields = ('last_name', 'first_name', 'id')
    def qr_code_image(self, obj):
        if obj.qr_code:
            return format_html(f'<img src="{obj.qr_code.url}" width="100" height="100" />')
        return "No QR Code"
    qr_code_image.short_description = "QR Code"

admin.site.register(Member, MemberAdmin)

# Register your models here.
