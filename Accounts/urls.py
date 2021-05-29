from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('sign-up/',views.signup,name="signup"),
    path('sign-up/<slug:username>',views.signup2,name="signup"),
    path('detail/',views.detail,name="detail"),
    path('login/',views.login1, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),

]
