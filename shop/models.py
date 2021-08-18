from io import open_code
from django.db import models
from Knell import settings
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField


# Product model
class Product(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the product")
    price = models.IntegerField(help_text="Price of the product")
    brand = models.CharField(max_length=100, help_text="Manufacturer of the product")
    category = models.CharField(max_length=100, help_text="Category of the product")
    picture = models.CharField(max_length=100, help_text="URL to the product picture") # Like "product_pictures/picture_name.png"
    warranty = models.CharField(max_length=30, help_text="Warranty length")
    shipping = models.BooleanField(help_text="Indicates if shipping is free or not")
    description = models.TextField(help_text="Description of product")

    def __str__(self):
        return self.name

# Single order model that fits single product
class orderProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

# Model containing orderProduct as cart items
class Order(models.Model):
    ref_code = models.CharField(max_length=32)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(orderProduct)

    def cart_list(self):
        return self.products.all()

    def __str__(self):
        return f"Order reference number: {self.ref_code} /n {self.products.all()}"

# Model saving completed orders
class orderHistory(models.Model):
    ref_code = models.CharField(max_length=32)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    products = models.ManyToManyField(orderProduct)
    date_ordered = models.DateTimeField(auto_now=True)
    price = models.IntegerField(null=False)

    def cart_list(self):
        return self.products.all()

    def __str__(self):
        return f"{self.ref_code}"

# Model for user profile data
class userProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    profile_picture = ResizedImageField(size=[250, 250], upload_to="user_pictures/", default="default_profile_picture.png")
    bio = models.TextField(max_length=500, blank=True)

class Review(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Reviewed product")
    content = models.CharField(max_length=300, help_text="Review of a product")
    rating = models.IntegerField(help_text="Rating of product")

    def __str__(self):
        return f"{self.content}"