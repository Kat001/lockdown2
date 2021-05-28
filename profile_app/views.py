from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password


from django.contrib import messages
import datetime
from datetime import date
from django.db.models import Sum


# models.......
from .models import Fund,DirectIncome,LevelIncome,FundTransferHistory,DirectIncome,PurchasedPackages,AllRoiIncome,AllRoiOnRoiIncome
from Accounts.models import Account



# Create your views here.
@login_required
def profile(request):
    user = request.user
    date_joined = str(user.date_joined)[0:10]
    d = {
        'user':user,
        'date_joined':date_joined
    }
    return render(request,'profile_templates/profile.html',d)

def personalInfo(request):
    user = request.user

    d = {
        'user':user
    }
    return render(request,'profile_templates/personalinfo.html',d)

def updateProfile(request):
    user = request.user
    name = user.username
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        mobile_no = request.POST.get('mobile')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')
        myfile = request.FILES['myfile']
        p = request.POST.get('txn_pass')

        
        if p == user.txn_password:
            user.first_name = f_name
            user.last_name = l_name
            user.phon_no = mobile_no
            user.address = address
            user.state = state
            user.city = city
            user.zip = zip
            user.image = myfile


            user.save()


            messages.success(request,'Profile Updated successfully!!')
            return redirect('updateprofile')
        else:
            messages.error(request,'Wrong Transection password!!')
            return redirect('updateprofile')
    else:
        pass

    d = {
        'user':user
    }
    return render(request,'profile_templates/updateprofile.html',d)

def updateKyc(request):
    return render(request,'profile_templates/updatekyc.html')

@login_required()
def changePassword(request):
    user = request.user
    user_pass = user.password

    if request.method == 'POST':
        o_pass = request.POST.get('o_pass')
        n_pass = request.POST.get('n_pass')
        c_pass = request.POST.get('c_pass')

        cheak = user.check_password(o_pass)

        if cheak:
            if n_pass == c_pass:
                p = make_password(n_pass)
                user.set_password(n_pass)
                user.save()
                update_session_auth_hash(request,user)
                messages.success(request,"Password Changed successfully!!")
                return redirect('changepassword')
            else:
                messages.error(request,'New password and confirm password should be same!!')
                return redirect('changepassword')
        else:
            messages.error(request,"Old Password is Wrong!!")
            return redirect('changepassword')


    return render(request,'profile_templates/changepassword.html')

def changeTransectionPassword(request):
    user = request.user
    user_t_pass = user.txn_password

    if request.method == 'POST':
        o_pass = request.POST.get('o_pass')
        n_pass = request.POST.get('n_pass')
        c_pass = request.POST.get('c_pass')

        if user_t_pass == o_pass:
            if n_pass == c_pass:
                user.txn_password = n_pass
                user.save()
                messages.success(request,'Txn password changed successfully!!')
            else:
                messages.error(request,'New password and confirm password should be same!!')
                return redirect('changetransectionpassword')
        else:
            messages.error(request,'Old Txn Password is Wrong!!')
            return redirect('changetransectionpassword')

    return render(request,'profile_templates/changetransectionpassword.html')

def activate(request):
    user = request.user
    fund_obj = Fund.objects.get(user = user)
    avail_fund = fund_obj.available_fund

    try:
        if request.method == 'POST':
            price = request.POST.get('pack')
            username = request.POST.get('u_name')
            activated_obj = Account.objects.get(username=username)
            password = request.POST.get('txn_pass')
            u_txn = user.txn_password

            if password == u_txn:
                if activated_obj.is_active1 == False:
                    if avail_fund >= int(price):
                        fund_obj.available_fund -= int(price)
                        activated_obj.is_active1 = True
                        activated_obj.activation_amount += int(price)
                        activated_obj.date_active = datetime.datetime.now()
                        activated_obj.save()
                        fund_obj.save()

                        # Assign Direct Income...............
                        sponsor_obj = activated_obj.sponsor
                        sponsor_obj.total_direct_income += (float(price)*10/100)
                        directIncome_obj = DirectIncome(user = sponsor_obj,activated_user = activated_obj,amount=(float(price)*5/100))
                        directIncome_obj.save()

                        # Assignment for Purchased Packages..............
                        totalProfit = 0
                        percent10 = 0
                        
                        if int(price) == 50:
                            totalProfit = 1000
                            percent10 = 50

                        elif int(price) == 1000:
                            totalProfit = 2000
                            percent10 = 100

                        elif int(price) == 2000:
                            totalProfit = 4200
                            percent10 = 200

                        elif int(price) == 5000:
                            totalProfit = 11250
                            percent10 = 500

                        elif int(price) == 10000:
                            totalProfit = 25000
                            percent10 = 1000

                        elif int(price) == 25000:
                            totalProfit = 68750
                            percent10 = 2500

                        elif int(price) == 50000:
                            totalProfit = 150000
                            percent10 = 5000

                        elif int(price) == 100000:
                            totalProfit = 300000
                            percent10 = 10000

                        purchasedpackages = PurchasedPackages(user = activated_obj,amount = int(price),profit=totalProfit,percent10= percent10)
                        purchasedpackages.save()

                        # Assign Level Income................
                        i = 5
                        obj = activated_obj
                        while obj.sponsor != None and i!=0:
                            obj = obj.sponsor
                            if obj.is_active1:
                                if i==5:
                                    income = (int(price)*5/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    levelIncome_obj = LevelIncome(user = obj,level='1',amount=income,activated_user=activated_obj)
                                    levelIncome_obj.save()
                                if i==4:
                                    income = (int(price)*2/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    levelIncome_obj = LevelIncome(user = obj,level='2',amount=income,activated_user=activated_obj)
                                    levelIncome_obj.save()
                                if i==3:
                                    income = (int(price)*1/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    levelIncome_obj = LevelIncome(user = obj,level='3',amount=income,activated_user=activated_obj)
                                    levelIncome_obj.save()
                                if i==2:
                                    income = (int(price)*1/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    levelIncome_obj = LevelIncome(user = obj,level='4',amount=income,activated_user=activated_obj)
                                    levelIncome_obj.save()

                                if i==1:
                                    income = (int(price)*1/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    levelIncome_obj = LevelIncome(user = obj,level='5',amount=income,activated_user=activated_obj)
                                    levelIncome_obj.save()
                                i = i - 1
                                obj.save()
                            else:
                                i = i - 1
                        messages.success(request,'Activated successfully!!')
                        return redirect('activate')


                    else:
                        messages.error(request,'Not Enough balance!!')
                        return redirect('activate')
                else:
                    messages.error(request,'Already Active!!')
                    return redirect('activate')


            else:
                messages.error(request,'Wrong transection password!!')
                return redirect('activate')

        else:
            pass



    except Exception as e:
        print(e)
        messages.error(request,str(e))
        return redirect('activate')

    d = {
        'fund_obj':fund_obj,
    }


    return render(request,'profile_templates/activate.html',d)


def directTeam(request):
    user = request.user
    directUsers = Account.objects.filter(sponsor = user)
    page = request.GET.get('page', 1)
    paginator = Paginator(directUsers, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    d = {
        'users':users,
        }

    return render(request,'profile_templates/directteam.html',d)



def fundTransfer(request):
    user = request.user
    obj = Fund.objects.get(user=user)

    if request.method == 'POST':
        username       = request.POST.get('user_name')
        amount          = request.POST.get('amount')
        txn_pass        = request.POST.get('txn_pass')

        try:
            if user.txn_password == txn_pass:
                if username != user.username:
                    user1 = Account.objects.get(username=username)
                    u_id_obj = Fund.objects.get(user=user1)

                    if obj.available_fund >= int(amount):
                        u_id_obj.available_fund += int(amount)
                        obj.available_fund -= int(amount)
                        u_id_obj.save()
                        obj.save()

                        obj_hist = FundTransferHistory(user=user,transfer_user=user1,amount=int(amount))
                        obj_hist.save()

                        messages.success(request,'Fund Transfered successfully!!')
                        return redirect('fundtransfer')

                    else:
                        messages.error(request,'Not Enough Amount!!')
                        return redirect('fund_transfer')
                else:
                    messages.error(request,'U entered your own id!!')
                    return redirect('fundtransfer')
            else:
                messages.error(request,'Wrong Txn Password!!')
                return redirect('fundtransfer')
        except Exception as e:
            print(e)
            messages.error(request,'User id does not exist!!')
            return redirect('fundtransfer')

    d = {
        'obj' : obj,
    }
    return render(request,'profile_templates/fundtransfer.html',d)


def fundTransferHistory(request):
    user = request.user
    userTransfer_obj = FundTransferHistory.objects.filter(user=user)
    page = request.GET.get('page', 1)
    paginator = Paginator(userTransfer_obj, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    d = {
        'users':users
    }  
    return render(request,'profile_templates/fundtransferhistory.html',d)
    


def directIncome(request):
    user = request.user
    direct_income = DirectIncome.objects.filter(user = user)

    page = request.GET.get('page', 1)
    paginator = Paginator(direct_income, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    d = {
        'users':users
    }
    return render(request,'profile_templates/directincome.html',d)

def levelIncome(request):
    user = request.user
    direct_income = LevelIncome.objects.filter(user = user)

    page = request.GET.get('page', 1)
    paginator = Paginator(direct_income, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    d = {
        'users':users
    }
    return render(request,'profile_templates/levelincome.html',d)


def RoiIncome(request):
    user = request.user
    roi_income = AllRoiIncome.objects.filter(user = user)

    page = request.GET.get('page', 1)
    paginator = Paginator(roi_income, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    d = {
        'users':users,
        'roi_income':roi_income
    }
    return render(request,'profile_templates/roiincome.html',d)

def RoiBoosterIncome(request):
    user = request.user
    roi_income = AllRoiOnRoiIncome.objects.filter(user = user)

    page = request.GET.get('page', 1)
    paginator = Paginator(roi_income, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    d = {
        'users':users,
        'roi_income':roi_income
    }
    return render(request,'profile_templates/roiincome.html',d)
    return render(request, "profile_templates/roiboosterincome.html", context)

def levelTeam1(request):
    user = request.user
    directUsers = Account.objects.filter(sponsor = user)
    page = request.GET.get('page', 1)
    paginator = Paginator(directUsers, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    d = {
        'users':users,
        }

    

    return render(request,'profile_templates/levelteam1.html',d)

def levelTeam2(request):
    user = request.user
    l = []

    objs1 = Account.objects.filter(sponsor=user)

    for o in objs1:
        obj2 = Account.objects.filter(sponsor=o)
        for i in obj2:
            l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    page = request.GET.get('page', 1)
    paginator = Paginator(objs, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    # myfilter = Account_Filter(request.GET,queryset=objs)
    # objs  = myfilter.qs

    d = {
        'users' : users,
    }
    return render(request,'profile_templates/levelteam2.html',d)

def levelTeam3(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponsor=user)

    for o in objs1:
        obj2 = Account.objects.filter(sponsor=o)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponsor=o2)
            for i in obj3:
                l.append(i.id)
    objs = Account.objects.filter(id__in=l)
    page = request.GET.get('page', 1)
    paginator = Paginator(objs, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    # myfilter = Account_Filter(request.GET,queryset=objs)
    # objs  = myfilter.qs

    d = {
        'users':users,
        
    }
    return render(request,'profile_templates/levelteam3.html',d)

def levelTeam4(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponsor=user)

    for o in objs1:
        obj2 = Account.objects.filter(sponsor=o)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponsor=o2)
            for o3 in obj3:
                obj4 = Account.objects.filter(sponsor=o3)
                for i in obj4:
                    l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    page = request.GET.get('page', 1)
    paginator = Paginator(objs, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)



    

    # myfilter = Account_Filter(request.GET,queryset=objs)
    # objs  = myfilter.qs

    d = {
        'users':users,
    }
    return render(request,'profile_templates/levelteam4.html',d)

def levelTeam5(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponsor=user)

    for o in objs1:
        obj2 = Account.objects.filter(sponsor=o)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponsor=o2)
            for o3 in obj3:
                obj4 = Account.objects.filter(sponsor=o3)
                for o4 in obj4:
                    obj5 = Account.objects.filter(sponsor=o4)
                    for i in obj5:
                        l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    page = request.GET.get('page', 1)
    paginator = Paginator(objs, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)



    # myfilter = Account_Filter(request.GET,queryset=objs)
    # objs  = myfilter.qs

    d = {
        'users':users,

    }
    return render(request,'profile_templates/levelteam5.html',d)
