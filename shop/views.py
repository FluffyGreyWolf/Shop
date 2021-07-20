from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, orderHistory, orderProduct, Order
from .utils import refCodeGenereator
from itertools import chain
from django.contrib.auth import get_user_model

# View for rendering main page
def home(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    order = Order.objects.get_or_create(owner=user)
    context = {'user': user, 'order': order}
    return render(request, 'base.html', context)

# View for searching products
def productSearch(request):
    if request.method == "GET":
        searched = request.GET['search-form']
        page_num = request.GET.get('page')
        if searched == "":
            return redirect('/')
        products1 = Product.objects.filter(name__contains=searched)
        products2 = Product.objects.filter(category__contains=searched)
        products = products1 | products2
        products_paginator = Paginator(products, 2)
        page = products_paginator.get_page(page_num)
        context = {'page': page, 'searched': searched}
        return render(request, 'search-result.html', context)
    
# View for filtering products
def productPriceFilter(request):
    if request.method == "GET":
        min = request.GET['price-min']
        max = request.GET['price-max']
        searched = request.GET['products']
        order = request.GET['price-order']
        page_num = request.GET.get('page')
    if not min:
        min = 0
    if not max:
        max = 50000
    products1 = Product.objects.filter(name__contains=searched).filter(price__gte=min).filter(price__lte=max)
    products2 = Product.objects.filter(category__contains=searched).filter(price__gte=min).filter(price__lte=max)
    products = products1 | products2
    if order == 'low':
        products = products.order_by('price')
        products_paginator = Paginator(products, 2)
        page = products_paginator.get_page(page_num)
        context = {'page': page, 'searched': searched, 'order': 'low'}
    else:
        products = products.order_by('-price')
        products_paginator = Paginator(products, 2)
        page = products_paginator.get_page(page_num)
        context = {'page': page, 'searched': searched, 'order': 'high'}
    return render(request, 'search-result.html', context)

# View for detailed page of product
def productDetail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product-detail.html', context)

# View for rednering shopping cart page
def cart(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    order = Order.objects.get(owner=user)
    context = {'order': order}
    return render(request, 'cart.html', context)

# View for adding items to cart
def addToCartBuy(request, pk):
    user = get_object_or_404(get_user_model(), username=request.user)
    product = get_object_or_404(Product, pk=pk)
    ordered_item, status  = orderProduct.objects.get_or_create(product=product)
    user_order, status = Order.objects.get_or_create(owner=user)
    user_order.products.add(ordered_item)
    user_order.ref_code = refCodeGenereator()
    user_order.save()
    return redirect('cart')

def addToCart(request, pk):
    user = get_object_or_404(get_user_model(), username=request.user)
    product = get_object_or_404(Product, pk=pk)
    ordered_item, status  = orderProduct.objects.get_or_create(product=product)
    user_order, status = Order.objects.get_or_create(owner=user)
    user_order.products.add(ordered_item)
    user_order.ref_code = refCodeGenereator()
    user_order.save()
    return redirect('product-detail', pk)

# View for removing items from cart
def removeFromCart(request, pk):
    item_to_delete = orderProduct.objects.filter(pk=pk)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        return redirect('cart')

# View for checkout page
def checkout(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    order = Order.objects.get(owner=user)
    items = orderProduct.objects.filter(order=order)
    price = 0
    for item in items:
        price += item.product.price
    context = {'order': order, 'items': items, 'price': price}
    return render(request, 'checkout.html', context)

# View for fake-buying items
def buy(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    order = Order.objects.get(owner=user)
    order_history, status = orderHistory.objects.get_or_create(owner=user, ref_code=order.ref_code, is_ordered=True)
    items = orderProduct.objects.filter(order=order)
    for item in items:
        order_history.products.add(item)
    order_history.save()
    order.delete()
    return redirect('buy-success')

# View for displaying page after successful purchase
def buySuccess(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    orders = orderHistory.objects.filter(owner=user)
    order = Order.objects.get_or_create(owner=user)
    context = {'orders': orders}
    return render(request, 'buy-success.html', context)