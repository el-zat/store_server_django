from django.shortcuts import render
from rest_framework.generics import ListAPIView

from products.models import Product
from products.serializers import ProductSerializer
# Create your views here.

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer