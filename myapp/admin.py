from django.contrib import admin
from .models import *
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'show_image_html', 'user', 'First_Name',  'Last_Name', ]
 

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category','name', 'price','show_image_html']
    fieldsets = (
    (None, {'fields': ['name', 'description', 'price']}),
    ('Category', {'fields': ['category']}),('Image', {'fields': ['image']}))
    list_filter = ['category']
    search_fields = ['name']

class OrderItemStqackedInlien(admin.StackedInline):
    model = OrderItem

class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    extra = 2

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status','customer', 'table_no',  'get_cert_items', 'get_cart_total', 'date_created']
    search_fields = ['id'] 
    list_filter = ['date_created', 'status']
    inlines = [ OrderItemTabularInline ]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id',  'product', 'order', 'quantity', 'get_total','date_created']
    list_filter = ['product', 'date_created']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_category_total']


class BookTableAdmin(admin.ModelAdmin):
    list_display = ['id', 'status','customer', 'people','date_time', 'timeBook']
    list_filter = ['date_time', 'timeBook', 'status']



admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BookTable, BookTableAdmin)