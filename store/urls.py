from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),  # إضافة المنتج للسلة
    path('cart/', views.view_cart, name='view_cart'),  # عرض السلة
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('order/<int:pk>/', views.confirm_order, name='confirm_order'),
    path('', views.product_list, name='product_list'),

]