from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product
from itertools import chain

# Main page view
def home(request):
    return render(request, 'base.html')

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