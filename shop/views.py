from django.shortcuts import render
from .models import Product

# Create your views here.
def home(request):
    return render(request, 'base.html')

def productSearch(request):
    if request.method == "GET":
        searched = request.GET['search-form']
        products = Product.objects.filter(name__contains=searched)
        context = {'searched': searched, 'products': products}
        return render(request, 'search-result.html', context)
    