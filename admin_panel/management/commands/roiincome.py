from django.core.management.base import BaseCommand
from django.utils import timezone
from profile_app.models import PurchasedPackages,AllRoiIncome,AllRoiOnRoiIncome


class Command(BaseCommand):
    help = 'Update Roi Income'

    def send_roi_on_roi(self,roi_obj):
        try:
            i = 5
            obj = roi_obj.user
            while obj.sponsor != None and i!=0:
                obj = obj.sponsor
                if obj.is_active1:
                    if i==5:
                        income = ((roi_obj.amount*10)/100)
                        # obj.total_level_income += income
                        # obj.refund += income
                        allroionroi_obj = AllRoiOnRoiIncome(user = obj,from_user=roi_obj.user,level='1',income=income,amount=roi_obj.amount)
                        allroionroi_obj.save()
                    if i==4:
                        income = ((roi_obj.amount*10)/100)
                        # obj.total_level_income += income
                        # obj.refund += income
                        allroionroi_obj = AllRoiOnRoiIncome(user = obj,from_user=roi_obj.user,level='2',income=income,amount=roi_obj.amount)
                        allroionroi_obj.save()
                    if i==3:
                        income = ((roi_obj.amount*10)/100)
                        # obj.total_level_income += income
                        # obj.refund += income
                        allroionroi_obj = AllRoiOnRoiIncome(user = obj,from_user=roi_obj.user,level='3',income=income,amount=roi_obj.amount)
                        allroionroi_obj.save()
                    if i==2:
                        income = ((roi_obj.amount*10)/100)
                        # obj.total_level_income += income
                        # obj.refund += income
                        allroionroi_obj = AllRoiOnRoiIncome(user = obj,from_user=roi_obj.user,level='4',income=income,amount=roi_obj.amount)
                        allroionroi_obj.save()
                    if i==1:
                        income = ((roi_obj.amount*10)/100)
                        # obj.total_level_income += income
                        # obj.refund += income
                        allroionroi_obj = AllRoiOnRoiIncome(user = obj,from_user=roi_obj.user,level='5',income=income,amount=roi_obj.amount)
                        allroionroi_obj.save()
                                
                else:
                    i = i - 1        
        except exception as e:
            print(e)

    def handle(self, *args, **kwargs):
        try:
            packages = PurchasedPackages.objects.all()
            
            for package in packages:
                # Day1 Income...................
                if package.day1:
                    roi_obj = AllRoiIncome(user = package.user,amount = ((package.amount*10)/100), package_amount = package.amount)
                    package.day1 = False
                    package.days -= 1
                    package.total_income += ((package.amount*10)/100)
                    package.save()
                    roi_obj.save()
                    # self.send_roi_on_roi(roi_obj)
                
                else:
                    # Income If User has not Withdrawaled any money
                    if package.is_withdrawal == False:
                        if package.days > 0:
                            income = (package.total_income*10)/100
                            roi_obj = AllRoiIncome(user = package.user,amount = income, package_amount = package.amount)
                            package.total_income += income
                            package.days -= 1
                            package.save()
                            roi_obj.save()
                            # self.send_roi_on_roi(roi_obj)

                        else:
                            pass
                    else:
                        # Income after first Withdarawl..............
                        if package.days > 0:
                            income = (package.amount*1)/100
                            roi_obj = AllRoiIncome(user = package.user,amount = income, package_amount = package.amount)
                            package.total_income += income
                            package.days -= 1
                            package.save()
                            roi_obj.save()
                            # self.send_roi_on_roi(roi_obj)
                        else:
                            pass
            
                

        except Exception as e:
            pass
        
        print("Done!!!!!")
