from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.order_root),
    path('orders/', views.order_list, name='orders'),
    path('orders/new', views.order_item, name='orders'),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/profile/', views.order_root)
]