from django.urls import path

from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('products/', views.product, name = 'product'),  # Product listing (no view name given)
    path('customer/<str:pk>/', views.customer, name='customer'),  # Customer detail view by pk
    
    path('account/', views.account_settings, name= 'account'), #account_setting is called from def account_settings 

    path('create-order/<str:pk>/', views.create_order, name='create_order'),  # Order creation page
    path('update-order/<str:pk>/', views.update_order, name='update_order'),  # Update order by pk
    path('delete-order/<str:pk>/', views.delete_order, name='delete_order'),  # Delete order by pk
    
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name = 'user_page'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),    
]
