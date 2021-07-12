from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('search-result', views.productSearch, name='search-result'),
    path('product-detail/<int:pk>', views.productDetail, name='product-detail'),
]