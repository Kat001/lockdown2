
from django.db import models
from Accounts.models import Account

# Create your models here.


class Payment_Fund(models.Model):
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    amount = models.CharField(max_length=100 , blank=True)
    order_id = models.CharField(max_length=1000 )
    razorpay_payment_id = models.CharField(max_length=1000 ,blank=True)
    paid = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='Purchase Date', auto_now_add=True)
    
    
    def __str__(self):
        return self.user.username