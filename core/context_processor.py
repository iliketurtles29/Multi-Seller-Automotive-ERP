from core.models import Product, Category, Vendor, CartOrder, CartOrderProducts, ProductImages, ProductReview, wishlist_model, Address
from django.db.models import Min, Max
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    product = Product.objects.all()
    vendors = Vendor.objects.all()
    cart = CartOrder.objects.all()
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])


    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    try:
        wishlist= wishlist_model.objects.filter(user=request.user)
    except:
        # messages.warning(request, "Please login first.")
        wishlist = 0

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None


    return {
        'cart_total_amount': cart_total_amount, 
        'p': product,
        'categories': categories,
        'address': address,
        'vendors': vendors,
        'min_max_price': min_max_price,
        'wishlist': wishlist,
    }