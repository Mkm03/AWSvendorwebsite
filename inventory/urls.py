from django.urls import path, include
from .views import (
    sign_up, home, profile, create_vendor, create_product,
    vendor_list, product_list, vendor_detail, product_detail,
    update_vendor, update_product, delete_vendor, delete_product
)

urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('profile/', profile, name='profile'),
    path('vendors/create/', create_vendor, name='create_vendor'),
    path('products/create/', create_product, name='create_product'),
    path('vendors/', vendor_list, name='vendor_list'),
    path('vendors/<int:pk>/', vendor_detail, name='vendor_detail'),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('vendors/update/<int:pk>/', update_vendor, name='update_vendor'),
    path('vendors/delete/<int:pk>/', delete_vendor, name='delete_vendor'),
    path('products/update/<int:pk>/', update_product, name='update_product'),
    path('products/delete/<int:pk>/', delete_product, name='delete_product'),
]
