from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_total',)

class OrderModelAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline, )
    list_display = ('pk', 'status', 'assigned', 'total')
    list_filter = ('status', 'created_at')
    readonly_fields = ('total',)

admin.site.register(Order, OrderModelAdmin)
