from django.contrib import admin
from .models import Payment_Fund

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display        = ('user','amount','date_joined','order_id','razorpay_payment_id',"paid")
    search_fields 		= ('user',)
    list_filter 		= ()
    fieldsets 			= ()

admin.site.register(Payment_Fund,PaymentAdmin)
