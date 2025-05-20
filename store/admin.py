from django.contrib import admin
from .models import Product, Order, SiteVisit, ProductImage

# لعرض الصور الإضافية للمنتج داخل صفحة المنتج
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # عدد الفورمات الفاضية الجاهزة

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    inlines = [ProductImageInline]  # عرض الصور الإضافية جوه المنتج

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'product', 'order_time')

@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('date', 'count')
    ordering = ('-date',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
