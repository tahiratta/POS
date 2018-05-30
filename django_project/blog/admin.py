from blog.models import *
from django.contrib import admin
from . import models

# Register your models here.


# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'created_on')
#     search_fields = ['name', 'email']
#     ordering = ['-name']
#     list_filter = ['active']
#     date_hierarchy = 'created_on'


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email', 'address', 'brandName',)
    search_fields = ['name', 'email']
    ordering = ['-created_at']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    # filter_horizontal = ('tags',)
    # raw_id_fields = ('tags',)
    # prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('slug',)
    fields = ('name', 'contact', 'email', 'address', 'brandName',)  

class Supplier_LedgerAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'amount_paid',)
    search_fields = ['supplier', 'amount_paid']
    ordering = ['-created_at']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    # filter_horizontal = ('tags',)
    # raw_id_fields = ('tags',)
    # prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('slug',)
    fields = ( 'supplier', 'amount_paid',)   

class ProductAdmin(admin.TabularInline):
    model = Product
    extra = 0

class PurchaseAdmin(admin.ModelAdmin):
    inlines = [ProductAdmin]


    # list_display = ('supplier', 'totalBill', 'discount', 'paidAmount',)
    # search_fields = ['supplier', 'paidAmount']
    # ordering = ['-created_at']
    # list_filter = ['created_at']
    # date_hierarchy = 'created_at'
    # # filter_horizontal = ('tags',)
    # # raw_id_fields = ('tags',)
    # # prepopulated_fields = {'slug': ('title',)}
    # # readonly_fields = ('slug',)
    # fields = ( 'supplier', 'totalBill', 'discount', 'paidAmount',)           

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description', 'barcode', 'brand', 'colour', 'cost', 'salePrice', 'quantity', 'bill')
#     search_fields = ['name', 'barcode', 'brand']
#     ordering = ['-created_at']
#     list_filter = ['created_at']
#     date_hierarchy = 'created_at'
#     # filter_horizontal = ('tags',)
#     # raw_id_fields = ('tags',)
#     # prepopulated_fields = {'slug': ('title',)}
#     # readonly_fields = ('slug',)
#     fields = ( 'name', 'description', 'barcode', 'brand', 'colour', 'cost', 'salePrice', 'quantity', 'bill')




class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email', 'address',)
    search_fields = ['name', 'email']
    ordering = ['-created_at']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    # filter_horizontal = ('tags',)
    # raw_id_fields = ('tags',)
    # prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('slug',)
    fields = ('name', 'contact', 'email', 'address',)

class Sale_ProductAdmin(admin.TabularInline):
    model = Sale_Product
    extra = 0     

class SaleAdmin(admin.ModelAdmin):
    inlines = [Sale_ProductAdmin]
    # list_display = ('customer', 'totalBill', 'discount', 'receivedAmount',)
    # search_fields = ['customer']
    # ordering = ['-created_at']
    # list_filter = ['created_at']
    # date_hierarchy = 'created_at'
    # # filter_horizontal = ('tags',)
    # # raw_id_fields = ('tags',)
    # # prepopulated_fields = {'slug': ('title',)}
    # # readonly_fields = ('slug',)
    # fields = ('customer', 'totalBill', 'discount', 'receivedAmount',)   

class Customer_LedgerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount_received',)
    search_fields = ['customer']
    ordering = ['-created_at']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    # filter_horizontal = ('tags',)
    # raw_id_fields = ('tags',)
    # prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('slug',)
    fields = ('customer', 'amount_received',)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer',)
    search_fields = ['customer']
    ordering = ['-created_at']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    # filter_horizontal = ('tags',)
    # raw_id_fields = ('tags',)
    # prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('slug',)
    fields = ('customer',)            

# admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Author)


admin.site.register(models.Supplier, SupplierAdmin)
admin.site.register(models.Supplier_Ledger, Supplier_LedgerAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
admin.site.register(models.Product)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Sale, SaleAdmin)
admin.site.register(models.Sale_Product)
admin.site.register(models.Customer_Ledger, Customer_LedgerAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)