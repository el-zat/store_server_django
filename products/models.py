from django.db import models
from users.models import User


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoriy"
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT)

    def __str__(self):
        return f'Product: {self.name} | Product category: {self.category.name}'

    class Meta:
        verbose_name_plural = "Products"


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        total_sum = sum([basket.sum() for basket in self.filter()])
        return total_sum

    def total_quantity(self):
        total_quantity = sum([basket.quantity for basket in self.filter()])
        return total_quantity


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Basket of {self.user.username} | Product: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
