from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('search-result', views.productSearch, name='search-result'),
    path('search-result-price-filter', views.productPriceFilter, name='search-result-price-filter'),
    path('product-detail/<int:pk>', views.productDetail, name='product-detail'),
    path('order-detail/<int:pk>', views.orderDetail, name='order-detail'),
    path('cart', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
    path('buy', views.buy, name="buy"),
    path('buy-success', views.buySuccess, name="buy-success"),
    path('add-to-cart/<int:pk>', views.addToCart, name='add-to-cart'),
    path('add-to-cart-buy/<int:pk>', views.addToCartBuy, name='add-to-cart-buy'),
    path('remove-from-cart/<int:pk>', views.removeFromCart, name='remove-from-cart'),
]