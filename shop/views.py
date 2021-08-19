from typing import Reversible
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, orderHistory, orderProduct, Order, Review, userProfile
from .utils import refCodeGenereator
from itertools import chain
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm

# View for rendering main page
def home(request):
    if request.user.is_authenticated:
        user = get_object_or_404(get_user_model(), username=request.user)
        order = Order.objects.get_or_create(owner=user)
        context = {'user': user, 'order': order}
    else:
        context = {}
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
    if request.user.is_authenticated:
        user = get_object_or_404(get_user_model(), username=request.user)
        user_review = Review.objects.filter(owner=user, product=product)
        pucharsed = orderHistory.objects.filter(owner=user)
        user_products = []
        for item in pucharsed:
            for item in item.cart_list():
                user_products.append(item)
        
        for item in user_products:
            if product.name == item.product.name:
                pucharsed = True
                break
            else:
                pucharsed = False
    else:
        user_review = None
        pucharsed = False
    reviews = Review.objects.filter(product=product)
    context = {'product': product, 'user_review': user_review, 'reviews': reviews, 'pucharsed': pucharsed}
    return render(request, 'product-detail.html', context)

# View for rednering shopping cart page
@login_required(login_url='/account/login/')
def cart(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    order = Order.objects.get(owner=user)
    context = {'order': order}
    return render(request, 'cart.html', context)

# View for adding items to cart by BUY NOW button
@login_required(login_url='/account/login/')
def addToCartBuy(request, pk):
    user = get_object_or_404(get_user_model(), username=request.user)
    product = get_object_or_404(Product, pk=pk)
    ordered_item, status  = orderProduct.objects.get_or_create(product=product)
    user_order, status = Order.objects.get_or_create(owner=user)
    user_order.products.add(ordered_item)
    user_order.ref_code = refCodeGenereator()
    user_order.save()
    return redirect('cart')

# View for adding items to cart by ADD TO CART button
@login_required(login_url='/account/login/')
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
@login_required(login_url='/account/login/')
def removeFromCart(request, pk):
    item_to_delete = orderProduct.objects.filter(pk=pk)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        return redirect('cart')

# View for checkout page
@login_required(login_url='/account/login/')
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
@login_required(login_url='/account/login/')
def buy(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    order = Order.objects.get(owner=user)
    items = orderProduct.objects.filter(order=order)
    price = 0
    for item in items:
        price += item.product.price
    order_history, status = orderHistory.objects.get_or_create(owner=user, ref_code=order.ref_code, is_ordered=True, price=price)
    for item in items:
        order_history.products.add(item)
    order_history.save()
    order.delete()
    return redirect('buy-success')

# View for displaying page after successful purchase
@login_required(login_url='/account/login/')
def buySuccess(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    orders = orderHistory.objects.filter(owner=user)
    order = Order.objects.get_or_create(owner=user)
    context = {'orders': orders}
    return render(request, 'buy-success.html', context)

# View for detailed page of order
@login_required(login_url='/account/login/')
def orderDetail(request, pk):
    order = get_object_or_404(orderHistory, pk=pk)
    context = {'order': order}
    return render(request, 'order-detail.html', context)

# View for creating review of product
@login_required(login_url='/account/login/')
def createReview(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user = get_object_or_404(get_user_model(), username=request.user)
    picture = get_object_or_404(userProfile, user=user)
    try:
        review = get_object_or_404(Review, product=product, owner=user)
    except:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        
        if form.is_valid():
            updated_form = form.save(False)
            updated_form.product = product
            updated_form.owner = user
            updated_form.profile_picture = picture.profile_picture
            updated_form.save()
            return redirect("product-detail", product.pk)
    else:
        form = ReviewForm()

    context = {'product': product, 'form': form, 'instance': review}
    return render(request, 'create-review.html', context)

# View for removing review of product
@login_required(login_url='/account/login/')
def removeReview(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user = get_object_or_404(get_user_model(), username=request.user)
    user_review = Review.objects.filter(owner=user, product=product)
    user_review.delete()
    return redirect("product-detail", product.pk)