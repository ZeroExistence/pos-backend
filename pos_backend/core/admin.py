from django.contrib import admin
from .models import Product, VariantType, Item, Variant

# Register your models here.

admin.site.register(Product)
admin.site.register(VariantType)


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0


class ItemModelAdmin(admin.ModelAdmin):
    inlines = (VariantInline, )
    list_display = ('product', 'price', 'sku', 'get_variant')
    list_filter = ('product',)


admin.site.register(Item, ItemModelAdmin)
