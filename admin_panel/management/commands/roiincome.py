from django.core.management.base import BaseCommand
from django.utils import timezone
from profile_app.models import PurchasedPackages,AllRoiIncome,AllRoiOnRoiIncome


class Command(BaseCommand):
    help = 'Update Roi Income'

    def send_roi_on_roi(self,roi_obj):
        try:
         sponsor_obj = roi_obj.user.sponsor
         income = (roi_obj.amount*10)/100
         obj = AllRoiOnRoiIncome(user=sponsor_obj,from_user=roi_obj.user,amount=roi_obj.amount,income=income)
         sponsor_obj.refund += income
         sponsor_obj.spn_roi_income += income
         obj.save()  
         sponsor_obj.save()     
        except exception as e:
            print(e)

    def handle(self, *args, **kwargs):
        try:
            packages = PurchasedPackages.objects.all()
            print(packages)
            for package in packages:
                if package.days > 0:
                    income = (package.amount*4)/100
                    income_obj = AllRoiIncome(user=package.user,amount=income,package_amount=package.amount)
                    user = package.user
                    user.total_roi_income += income
                    user.refund += income
                    income_obj.save()
                    user.save()
                    self.send_roi_on_roi(income_obj)
        except Exception as e:
            print(e)

    # def handle(self, *args, **kwargs):
    #     try:
    #         packages = PurchasedPackages.objects.all()
            
    #         for package in packages:
    #             # Day1 Income...................
    #             if package.day1:
    #                 roi_obj = AllRoiIncome(user = package.user,amount = ((package.amount*10)/100), package_amount = package.amount)
    #                 package.day1 = False
    #                 package.days -= 1
    #                 package.total_income += ((package.amount*10)/100)
    #                 user = package.user
    #                 user.refund += ((package.amount*10)/100)
    #                 user.total_roi_income += ((package.amount*10)/100)
    #                 user.save()
    #                 package.save()
    #                 roi_obj.save()
    #                 self.send_roi_on_roi(roi_obj)
                
    #             else:
    #                 # Income If User has not Withdrawaled any money
    #                 if package.is_withdrawal == False:
    #                     if package.days > 0:
    #                         income = (package.total_income*10)/100
    #                         roi_obj = AllRoiIncome(user = package.user,amount = income, package_amount = package.amount)
    #                         package.total_income += income
    #                         package.days -= 1
    #                         user = package.user
    #                         user.refund += income
    #                         user.total_roi_income += income
    #                         user.save()
    #                         package.save()
    #                         roi_obj.save()
    #                         self.send_roi_on_roi(roi_obj)
    #                     else:
    #                         pass
    #                 else:
    #                     # Income after first Withdarawl..............
    #                     if package.days > 0:
    #                         income = (package.amount*1)/100
    #                         roi_obj = AllRoiIncome(user = package.user,amount = income, package_amount = package.amount)
    #                         package.total_income += income
    #                         package.days -= 1
    #                         user = package.user
    #                         user.refund += income
    #                         user.total_roi_income += income
    #                         user.save()
    #                         package.save()
    #                         roi_obj.save()
    #                         self.send_roi_on_roi(roi_obj)
    #                     else:
    #                         pass
            
        except Exception as e:
            pass
        
        print("Done!!!!!")
