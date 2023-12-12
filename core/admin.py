from django.contrib import admin
from core.models import Product, slider , Category, Vendor ,CartOrder, CartOrderProducts, ProductImages, ProductReview, wishlist_model, Address
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

admin.site.site_title = "Billie Moto"
admin.site.site_header = "Billie Moto"

# Register your models here.


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If it's a new object being created
            obj.user = request.user  # Set the user as the currently logged-in user
            obj.vendor = request.user.vendor_set.first()  # Get the associated Vendor for the user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:  # Allow superuser to see all products
            qs = qs.filter(vendor__user=request.user)
        return qs
    
    inlines = [ProductImagesAdmin]
    list_display = ['title', 'product_image', 'price', 'category', 'stock_count','vendor', 'featured', 'product_status']
    # list_editable = ['product_status', 'price', 'stock_count']
    readonly_fields = ['user', 'vendor', 'pid', 'date', 'updated' , 'sold_item' , 'total_product_sale']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    


class VendorAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Get the original queryset
        queryset = super().get_queryset(request)
        
        # If the user is not a superuser, filter the queryset based on the logged-in user
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)  # Adjust 'user' to the field you want to filter on

        return queryset

    list_display = ['title', 'vendor_image']
    readonly_fields = ['vid', 'sales', 'user']



class CartOrderProductsAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If it's a new object being created
            # Get the associated Product for the CartOrderProduct item
            product = Product.objects.filter(title=obj.item).first()
            # Assign the vendor from the associated Product
            if product:
                obj.vendor = product.vendor
        super().save_model(request, obj, form, change)

    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(vendor__user=request.user)
        return queryset
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If it's a new object being created
            # Get the associated Product for the CartOrderProduct item
            product = Product.objects.filter(title=obj.item).first()
            # Assign the vendor from the associated Product
            if product:
                obj.vendor = product.vendor

    def save_model(self, request, obj, form, change):
        # ... (existing code)

        # If the product status is changed to 'Delivered'
        if change and 'product_status' in form.changed_data and obj.product_status == 'Delivered':
            # Get the associated user's email from the address
            user_email = obj.address.user.email if obj.address and obj.address.user else None
            
            if user_email:
                subject = 'Your order has been delivered'
                message = f"Your order {obj.invoice_no} has been delivered.\n\n"
                message += "Order Details:\n"
                message += f"Item: {obj.item}\n"
                message += f"Quantity: {obj.qty}\n"
                message += f"Price: {obj.price}\n"
                message += f"Total: {obj.total}\n"
                # Add more order details as needed

                message += '\nThank you for shopping with us!'
                from_email = 'billiemoto.official@gmail.com'
                recipient_list = [user_email]

                # Send an email to the user
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        super().save_model(request, obj, form, change)
            
    
    list_display = ['invoice_no', 'order_date', 'vendor','item', 'qty', 'price', 'total', 'paid_status','product_status']
    # list_editable = ['paid_status', 'product_status']
    readonly_fields = ['vendor', 'invoice_no', 'order_date', 'vendor','item', 'qty', 'price', 'total', 'address', 'image', 'order', 'cancel_order']
      

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']


class wishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']


class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'mobile', 'status']
    list_display = ['user', 'address', 'mobile', 'status']

class FilteredCartOrderProducts(CartOrderProducts):
    
    class Meta:
        proxy = True

class FilteredCartOrderProductsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(vendor__user=request.user, product_status='Delivered')
        return queryset
    
    list_display = ['invoice_no', 'order_date', 'vendor', 'item', 'qty', 'price', 'total', 'paid_status', 'product_status']
    readonly_fields = ['vendor', 'invoice_no', 'order_date', 'vendor', 'item', 'qty', 'price', 'total', 'address', 'image', 'order']

# Register the proxy model and its admin in your admin.py file
admin.site.register(FilteredCartOrderProducts, FilteredCartOrderProductsAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
# admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderProducts, CartOrderProductsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(wishlist_model, wishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(slider)