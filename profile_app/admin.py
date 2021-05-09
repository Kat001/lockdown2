from django.contrib import admin
from .models import Fund,FundTransferHistory,DirectIncome,LevelIncome,PurchasedPackages,Bank_Info,AllRoiIncome,AllRoiOnRoiIncome,book

# Register your models here.

class FundAdmin(admin.ModelAdmin):
    list_display        = ('user','available_fund')
    search_fields 		= ('user',)
    list_filter 		= ()
    fieldsets 			= ()

class FundTransferHistoryAdmin(admin.ModelAdmin):
    list_display        = ('user','transfer_user','date','amount')
    search_fields 		= ('user',)
    list_filter 		= ()
    fieldsets 			= ()

class DirectIncomeAdmin(admin.ModelAdmin):
    list_display        = ('user','activated_user','date','amount')
    search_fields 		= ('user',)
    list_filter 		= ()
    fieldsets 			= ()

class LevelIncomeAdmin(admin.ModelAdmin):
    list_display        = ('user','activated_user','date','amount','level')
    search_fields 		= ('user',)
    list_filter 		= ()
    fieldsets 			= ()

class PurchasedPackagesAdmin(admin.ModelAdmin):
    list_display        = ('user','date','amount','profit','percent10','total_income','day1')
    search_fields 		= ('user',)
    list_filter 		= ()
    fieldsets 			= ()

class AllRoiIncomeAdmin(admin.ModelAdmin):
    list_display        = ('user','date','package_amount','amount')
    search_fields 		= ('user',)
    list_filter 		= ()
    fieldsets 			= ()

class AllRoiOnRoiIncomeAdmin(admin.ModelAdmin):
    list_display        = ('user','from_user','level','date','income','amount')
    search_fields 		= ('user',)
    list_filter 		= ()
    fieldsets 			= ()

class Bank_Info_Admin(admin.ModelAdmin):
    list_display 		= ('username','account_holder_name','account_number')
    search_fields 		= ('username',)
    list_filter 		= ()
    fieldsets 			= ()
    '''def has_delete_permission(self,request,obj=None):
            return False
    def has_add_permission(self,request,obj=None):
		return False'''



admin.site.register(book)
admin.site.register(Fund,FundAdmin)
admin.site.register(FundTransferHistory,FundTransferHistoryAdmin)
admin.site.register(DirectIncome,DirectIncomeAdmin)
admin.site.register(LevelIncome,LevelIncomeAdmin)
admin.site.register(PurchasedPackages,PurchasedPackagesAdmin)
admin.site.register(Bank_Info,Bank_Info_Admin)
admin.site.register(AllRoiIncome,AllRoiIncomeAdmin)
admin.site.register(AllRoiOnRoiIncome,AllRoiOnRoiIncomeAdmin)

