from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the product")
    price = models.IntegerField(help_text="Price of the product")
    brand = models.CharField(max_length=100, help_text="Manufacturer of the product")
    category = models.CharField(max_length=100, help_text="Category of the product")
    picture = models.CharField(max_length=100, help_text="URL to the product picture") # Like "/media/product_pictures/example.png"

    def __str__(self):
        return self.name