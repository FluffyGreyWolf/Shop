from django.db.models.query_utils import RegisterLookupMixin
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product
from itertools import chain

# Main page view
def home(request):
    return render(request, 'base.html')

# View for searching products
def productSearch(request):
    if request.method == "GET":
        searched = request.GET['search-form']
        if searched == "":
            return redirect('/')
        # Chaining filters won't work? - returns empty queryset
        products1 = Product.objects.filter(name__contains=searched)
        products2 = Product.objects.filter(category__contains=searched)
        products = list(chain(products1, products2))
        context = {'products': products, 'searched': searched}
        return render(request, 'search-result.html', context)
    
# View for filtering products by price
def productPriceFilter(request):
    if request.method == "GET":
        min = request.GET['price-min']
        max = request.GET['price-max']
        searched = request.GET['products']
    if not min:
        min = 0
    if not max:
        max = 50000
    products1 = Product.objects.filter(name__contains=searched).filter(price__gte=min).filter(price__lte=max)
    products2 = Product.objects.filter(category__contains=searched).filter(price__gte=min).filter(price__lte=max)
    products = list(chain(products1, products2))
    context = {'products': products, 'searched': searched}
    return render(request, 'search-result.html', context)




# View for detailed page of product
def productDetail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product-detail.html', context)