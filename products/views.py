from django.shortcuts import render
from products.models import Product, ProductCategory



# Create your views here.
def index(request):
    context = {
        'title': 'Store',
        'is_promotion': True,
    }
    return render(request, 'index.html', context)


def products(request):
    context = {
        'title': 'Products',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products.html', context)
