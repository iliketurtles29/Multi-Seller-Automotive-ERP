from django.db import models
from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from sys import prefix
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.dispatch import receiver
from django.db.models.signals import pre_save  # Add this line to import pre_save signal



STATUS_CHOICE = (
    ("Cancelled", "Cancelled"),
    ("Processing", "Order Placed"),
    ("Preparing", "Preparing to Ship"),
    ("Shipped", "In Transit"),
    ("Delivered", "Delivered"),
)

STATUS = (
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("published", "Published"),
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

class slider(models.Model):
    DISCOUNT_DEAL = (
        ("HOT DEALS", 'Hot Deals'),
        ("NEW ARRIVALS", 'New Arrivals'),
    )
    Image = models.ImageField(upload_to="slider_imgs")
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL, max_length=100)
    SALE = models.IntegerField()
    Brand_Name = models.CharField(max_length=200)
    Discount = models.IntegerField()

    def __str__(self):
        return self.Brand_Name
    


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=15, max_length=25, prefix="categ", alphabet="ahnmlvindecrz123")
    title = models.CharField(max_length=100, default="Automotive")
    categ_desc = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="category", default="category.png")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50"  height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    

    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=15, max_length=25, prefix="vend", alphabet="ahnmlvindecrz123")

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    description = RichTextUploadingField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True,blank=True)

    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    sales = models.IntegerField(default=0)
    

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Edit Shop"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50"  height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=15, max_length=25, alphabet="ahnmlvindecrz123")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="product")

    title = models.CharField(max_length=100, default="Helmet")
    image = models.ImageField(upload_to=user_directory_path, default="product.png")
    description = RichTextUploadingField(null=True, blank=True, default="this is a Product")

    price = models.DecimalField(max_digits=99999999, decimal_places=2, default="4.99")
    old_price = models.DecimalField(max_digits=99999999, decimal_places=2, default="7.99")

    stock_count = models.IntegerField(default="1")
    sold_item = models.IntegerField(default=0)
    total_product_sale = models.IntegerField(default=0)

    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    # tags = TaggableManager(blank=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=5, max_length=15, prefix="auto", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inventory"

    def product_image(self):
        return mark_safe('<img src="%s" width="50"  height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price
    
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.png")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"



#================================Carts Orders Addresses=======================================


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default="4.99")
    # paid_status = models.BooleanField(default=False)
    # order_date = models.DateField(auto_now_add=True)
    # product_status = models.CharField(choices=STATUS_CHOICE, max_length=35, default="Processing")
    # product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, related_name="cart_orders")

    class Meta:
        verbose_name_plural = "Cart Order"

    # def save(self, *args, **kwargs):
    #     # Set the vendor based on the associated product
    #     if self.product and not self.vendor:
    #         self.vendor = self.product.vendor
    #     super().save(*args, **kwargs)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=300, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    
    class Meta:
            verbose_name_plural = "Address"
    
class CartOrderProducts(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default="4.99")
    total = models.DecimalField(max_digits=9999999999, decimal_places=2, default="4.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=35, default="Processing")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="order_products")
    cancel_order = models.BooleanField(default=False)

    
    class Meta:
        verbose_name_plural = "Transactions"

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    

    

    #================================Carts Orders Addresses=======================================



class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"
    
    def get_rating(self):
        return self.rating
    

    
class wishlist_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name_plural = "Wishlists"
    
    def __str__(self):
        return self.product.title
