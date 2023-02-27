from django.contrib import admin
from . models import Login, Customer, Product, Category, ShoppingCart, Orders
#class AdminProduct(admin.ModelAdmin):
#    list_display= ['name','price','desc','category']

# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','desc','image']
class AdminCategory(admin.ModelAdmin):
    list_display=['name']

class AdminCustomer(admin.ModelAdmin):
    list_display = ['name', 'emailaddress', 'pincode', 'regdate']
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
class AdminOrders(admin.ModelAdmin):
    list_display=['customer','product','price','quantity','order_date']

class AdminShoppingCart(admin.ModelAdmin):
    list_display=['customer', 'product', 'quantity']

admin.site.register(Login)
admin.site.register(Customer,AdminCustomer)
admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(ShoppingCart, AdminShoppingCart)
admin.site.register(Orders, AdminOrders)