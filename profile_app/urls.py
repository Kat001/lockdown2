from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.profile,name='profile'),
   path('personal-info/',views.personalInfo,name='personalinfo'),
   path('update-profile/',views.updateProfile,name='updateprofile'),
   path('update-KYC/',views.updateKyc,name='updatekyc'),
   path('change-password/',views.changePassword,name='changepassword'),
   path('change-transection-password/',views.changeTransectionPassword,name='changetransectionpassword'),
   

   # Activation urls................
   path('add-fund/',include('payment.urls'),),
   path('activate-id/',views.activate,name='activate'),
   path('transfer-fund/',views.fundTransfer,name='fundtransfer'),
   path('transfer-fund-history/',views.fundTransferHistory,name='fundtransferhistory'),

   # Team Urls............
   path('direct-team/',views.directTeam,name='directteam'),
   path('level-team1/', views.levelTeam1, name='levelteam1'),
   path('level-team2/', views.levelTeam2, name='levelteam2'),
   path('level-team3/', views.levelTeam3, name='levelteam3'),
   path('level-team4/', views.levelTeam4, name='levelteam4'),
   path('level-team5/', views.levelTeam5, name='levelteam5'),

   #Income Urls...........
   path('direct-income/',views.directIncome,name='directincome'),
   path('level-income/',views.levelIncome,name='levelincome'),
   path('roi-income/',views.RoiIncome,name='roiincome'),
   path('roi-booster-income/',views.RoiBoosterIncome,name='roiboosterincome'),

   # Withdrawal History.......
   path('withdrawal-history/',views.withdrawalHistory,name='withdrawalhistory')

]
