from django.contrib.auth import views as auth_views
from django.urls import path
from dennisapp import views

urlpatterns = [
    path('settings',views.settings, name='settings'),
    path('users/',views.userpage, name='users'),
    path('login/',views.loginn, name='login'),
    path('logout/',views.logoutt, name='logout'),
    path('register/',views.register, name='register'),
    path('customer.html/<str:number>/',views.customer, name='customer'),
    path('products.html/',views.products, name='products'),
    path('', views.dashboard, name='dashboard'),
    path('form/<str:customerid>',views.dennisform, name='form'),
    path('createcustomer/', views.createcustomer, name='createcustomer'),
    path('updateorder/<str:customerid>', views.updateorderid, name='updateorder'),
    path('updateform/<str:customerid>',views.updatedennisform, name='updateform'),
    path('delete/<str:deleteid>',views.deleteitem, name='deleteitem'),

    path('reset_password/',auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]


