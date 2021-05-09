from django.shortcuts import render,redirect
import razorpay
from .models import Payment_Fund
from django.views.decorators.csrf import csrf_exempt
from profile_app.models import *
from Accounts.models import Account
from django.contrib import messages


# Create your views here.
@csrf_exempt
def payment(request):
    user = request.user
    userTxn = user.txn_password
    
    if request.method == 'POST':
        comment = request.POST.get('comment')
        clientTxn = request.POST.get('txn_pass')
        if userTxn == clientTxn:
            amount = int(request.POST.get('amount')) * 100

            client = razorpay.Client(auth= ('rzp_test_seOaAXPGw39Tu3','4nQRrscLjGZbxhrhgdM25XnN'))
            payment = client.order.create({'amount':amount, 'currency':'INR','payment_capture':'1' })
            
            obj = Payment_Fund(user = user,amount=amount,order_id=payment['id'])
            obj.save()
            return render(request,'payment.html',{'payment':payment})
        else:
            messages.error(request,'Transection password is not correct!!')
            return redirect('payment')



    return render(request,'payment.html',{'user':user})

def success(request):
    user = request.user
    if request.method == 'POST':
        order_id = request.POST['razorpay_order_id']
        payment_obj = Payment_Fund.objects.get(order_id=order_id)
        payment_obj.paid = True
        payment_obj.razorpay_payment_id = request.POST['razorpay_payment_id']
        payment_obj.save()

        fund_obj = Fund.objects.get(user = user)
        fund_obj.available_fund += int(payment_obj.amount)
        fund_obj.save()
        return render(request,'success.html')
    
    return render(request,'fail.html')
        
        
