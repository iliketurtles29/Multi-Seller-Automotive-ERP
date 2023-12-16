from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg
from core.models import Product, Category,slider ,User, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address, CartOrderProducts
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from userauths.forms import VendorRegistrationForm
from django.shortcuts import get_object_or_404
from userauths.models import Profile
from datetime import date
from django.db.models import Sum
from django.db.models import Count
from django.db import transaction
from django.utils.html import strip_tags
from django.core.mail import send_mail
# from django.urls import reverse
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from paypal.standard.forms import PayPalPaymentsForm


def index(request):
    #products = Product.objects.all().order_by("-id")
    #products = Product.objects.filter(featured=True)

    # Fetch other data for the index view
        
    # Count the products belonging to the current vendor
    product = Product.objects.all()
    sliders = slider.objects.all()
    products = Product.objects.filter(product_status="published").order_by("-date")
    categories = Category.objects.all()
    current_vendor = None  # Default to None if user is not authenticated or has no associated vendor profile

    if request.user.is_authenticated:
        try:
            current_vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            pass



    context = { 
        "p": product,
        "products": products,
        "categories": categories, 
        'sliders': sliders,
        "current_vendor":current_vendor 
    }

    return render(request, 'core/index.html', context)

@login_required
def index2(request):
    try:
        current_vendor = Vendor.objects.get(user=request.user)
        vendor_products = Product.objects.filter(vendor=current_vendor)

        vendor_products_count = vendor_products.count()
        vendor_users_count = User.objects.count()
        vendor_sales = current_vendor.sales  # Fetching total sales for the current vendor

        # Fetching sales for the current day/date only
        current_date = date.today()
        daily_sales = CartOrderProducts.objects.filter(
            order__user=request.user,
            order_date=current_date,
            vendor=current_vendor
        ).aggregate(total_sales=Sum('total'))['total_sales'] or 0

        # Counting CartOrderProducts for the current vendor (logged-in user)
        vendor_cart_orders_count = CartOrderProducts.objects.filter(vendor=current_vendor).exclude(product_status='Cancelled').count()


        context = {
            'vendor_products_count': vendor_products_count,
            'vendor_users_count': vendor_users_count,
            'vendor_sales': vendor_sales,
            'vendor_products': vendor_products,
            'daily_sales': daily_sales,  # Adding daily sales to the context
            'vendor_cart_orders_count': vendor_cart_orders_count,  # Adding vendor's cart orders count
             # Adding sold_item count for each product
        }
    except Vendor.DoesNotExist:
        context = {
            'vendor_products_count': 0,
            'vendor_users_count': 0,
            'vendor_sales': 0,
            'vendor_products': None,
            'daily_sales': 0,
            'vendor_cart_orders_count': 0,
          
        }

    return render(request, 'core/admin-dashboard.html', context)



def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    current_vendor = None  # Default to None if user is not authenticated or has no associated vendor profile

    if request.user.is_authenticated:
        try:
            current_vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            pass  # If no associated vendor profile found, 'current_vendor' remains as None

    context = {  
        "products": products,
        "categories": categories,
        'vendors': vendors,
        'current_vendor': current_vendor,  # Pass the current vendor to the template
    }

    return render(request, 'core/product-list.html', context)


def category_list_view(request):
   # categories = Category.objects.all()
    categories = Category.objects.all().annotate(product_count=Count("category"))

    context = {
        "categories": categories
    }
    return render(request, 'core/category-list.html', context)


def category_product_list__view(request, cid):
    product = Product.objects.all()
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)
    categories = Category.objects.all()

    current_vendor = None  # Default to None if user is not authenticated or has no associated vendor profile

    if request.user.is_authenticated:
        try:
            current_vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            pass
    

    context = {
        "p": product,
        "category": category,
        "products": products,
        "categories": categories,
        "current_vendor": current_vendor,
    }
    return render(request, "core/catgory-product-list.html", context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    categories = Category.objects.all()

    context ={
        "vendors": vendors,
        "categories": categories,
    }
    return render(request, "core/vendor-list.html", context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")
    categories = Category.objects.all()
    
    current_vendor = None  # Default to None if user is not authenticated or has no associated vendor profile

    if request.user.is_authenticated:
        try:
            current_vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            pass

    context ={
        "vendor": vendor,
        "products": products,
        "categories": categories,
        "current_vendor": current_vendor,
    }
    return render(request, "core/vendor-detail.html", context)

def product_detail_view(request, pid):
    product = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category=product.category)
    categories = Category.objects.all()

    reviews = ProductReview.objects.filter(product=product).order_by("-date") 
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    review_form = ProductReviewForm()
    make_review = True
    cart_order = None

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False
        
        # Check if the user has a delivered order for this product
        user_orders = CartOrderProducts.objects.filter(order__user=request.user, item=product)  # Adjust this line
        for order in user_orders:
            if order.product_status == 'Delivered':
                cart_order = order
                break
    
    current_vendor = None  # Default to None if user is not authenticated or has no associated vendor profile

    if request.user.is_authenticated:
        try:
            current_vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            pass

    context = {
        "p": product,
        "products": products,
        "make_review": make_review,
        "review_form": review_form,
        "average_rating": average_rating,
        "reviews": reviews,
        "categories": categories,
        "cart_order": cart_order,
        "current_vendor": current_vendor,
    }

    return render(request, "core/product-detail.html", context)

def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )
    

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
        'bool': True,
        'context': context,
        'average_reviews': average_reviews,
        }
    )


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")


    current_vendor = None  # Default to None if user is not authenticated or has no associated vendor profile

    if request.user.is_authenticated:
        try:
            current_vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            pass

    context ={
        "products": products,
        "query": query,
        "current_vendor": current_vendor,
    }

    return render(request, "core/search.html", context)


def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products =Product.objects.filter(product_status="published").order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        vendors = products.filter(vendor__id__in=vendors).distinct()

    current_vendor = None  # Default to None if user is not authenticated or has no associated vendor profile

    if request.user.is_authenticated:
        try:
            current_vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            pass


    data = render_to_string("core/async/product-list.html", {"products": products, "current_vendor": current_vendor})
    return JsonResponse({"data": data})

from django.http import JsonResponse

def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
        
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")
    
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = str(request.GET['qty'])

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

def redirect_to_multiple_urls(request):
    # First, clear the cart data
    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']

    # Then, redirect to the dashboard
    return redirect('core:dashboard')   

@login_required
def wishlist_view(request):
    product = Product.objects.all()
    wishlist_items = wishlist_model.objects.select_related('product').filter(user=request.user)
    wishlist = wishlist_model.objects.all()

    current_vendor = None  # Default to None if user is not authenticated or has no associated vendor profile

    if request.user.is_authenticated:
        try:
            current_vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            pass

    context = {
        "wishlist_items": wishlist_items,
        "p": product,
        "w": wishlist,
        "current_vendor": current_vendor,
    }
    return render(request, "core/wishlist.html", context)

def add_to_wishlist(request):
    product_id = request.GET["id"]
    product = Product.objects.get(id=product_id)

    context = {}

    wishlist_count = wishlist_model.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = wishlist_model.objects.create(
            product=product,
            user=request.user
        )
        context = {
            "bool": True
        }

    return JsonResponse(context)
    
@login_required
def checkout_view(request):
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except Address.DoesNotExist:
        active_address = None
        messages.warning(request, "Please set a default address before checkout.")
        return redirect('core:dashboard')  # Replace with your address setting URL

    

    return render(request, "core/checkout.html", {
        'active_address': active_address
    })


@login_required
def payment_completed_view(request):
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except Address.DoesNotExist:
        active_address = None
        messages.warning(request, "Please set a default address before checkout.")
        return redirect('core:dashboard')  # Replace with your address setting URL

    cart_total_amount = 0
    total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

            product = Product.objects.get(pk=p_id)
            if int(item['qty']) > product.stock_count:
                messages.warning(request, f"Quantity of {product.title} exceeds available stock.")
                return redirect('core:cart')

        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount,
        )

        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            product = Product.objects.get(pk=p_id)
            cart_order_product = CartOrderProducts.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=int(item['qty']) * float(item['price']),
                address=active_address,
            )

            # Set the vendor of CartOrderProducts to the associated product's vendor
            cart_order_product.vendor = product.vendor
            cart_order_product.save()

            vendor = product.vendor
            vendor.sales += int(item['qty']) * float(item['price'])  # Incrementing sales
            vendor.save()

            product.stock_count -= int(item['qty'])
            product.sold_item += int(item['qty'])
            product.total_product_sale += int(item['qty']) * float(item['price'])
            product.save()

            # Send email to the vendor/user
            vendor_user = product.vendor.user  # Retrieve the associated user (assuming vendor is associated with a User)
            vendor_email = vendor_user.email  # Retrieve the user's email

            subject = 'New Order Received'
            html_message = render_to_string('email_templates/order_notification.html', {
                'item_title': item['title'],
                'item_image':item['image'],
                'item_qty': item['qty'],
                'total_price': int(item['qty']) * float(item['price']),
                # Include any other relevant details you want to send in the email
            })
            plain_message = strip_tags(html_message)  # Strip HTML tags for the plain text version

            send_mail(subject, plain_message, 'billiemoto.official@gmail.com', [vendor_email], html_message=html_message)

    return render(request, "core/payment-completed.html", {
        "cart_data": request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'active_address': active_address
    })





def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')


def render_order_notification(request):
    # Logic to render your email template
    return render(request, 'email_templates/order_notification.html', {
        # context data if needed
    })

@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)
    delivered_orders = CartOrderProducts.objects.filter(order__user=request.user, product_status="Delivered").order_by("-order__id")
    cancelled_orders = CartOrderProducts.objects.filter(order__user=request.user, cancel_order=True).order_by("-order__id")

    if request.method == "POST":
        # Check if the request contains the vendor registration form
        vendor_form = VendorRegistrationForm(request.POST, request.FILES)
        if vendor_form.is_valid():
            vendor = vendor_form.save(commit=False)
            messages.success(request, "You are now a Vendor")
            # Assign the logged-in user to the vendor
            vendor.user = request.user
            vendor.save()
            # You can redirect to the dashboard or any relevant page
            return redirect("core:dashboard")

        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address added successfully.")
        return redirect("core:dashboard")
    
    user_profile = Profile.objects.get(user=request.user)

    context = {
        
        "user_profile": user_profile,
        "orders": orders,
        "address": address,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        "vendor_form": VendorRegistrationForm(),  # Add the vendor registration form to the context
    }
    return render(request, 'core/dashboard.html', context)

def order_detail(request):
    # Fetch all orders associated with the current user
    orders = CartOrder.objects.filter(user=request.user)

    # Fetch all order items associated with the fetched orders and the current user
    order_items = CartOrderProducts.objects.filter(order__user=request.user).order_by('-invoice_no')

    # Filter order_items based on product_status ("Order Placed," "Preparing to Ship," or "In Transit")
    STATUS_FILTER = ["Processing", "Preparing", "Shipped", "Order Placed", "Preparing to Ship", "In Transit"]
    filtered_order_items = order_items.filter(product_status__in=STATUS_FILTER)

    context = {
        "orders": orders,
        "order_items": filtered_order_items,
    }
    return render(request, 'core/order-detail.html', context)


@transaction.atomic
def cancel_order(request, order_item_id):
    if request.method == 'POST':
        order_item = get_object_or_404(CartOrderProducts, id=order_item_id)

        if not order_item.cancel_order:  # Check if the order is not already canceled
            order_item.cancel_order = True
            order_item.product_status = 'Cancelled' 
            order_item.save()

            # Fetch product information using the item string
            product_title = order_item.item  # Assuming item stores the product title
            try:
                product = Product.objects.get(title=product_title)
                # Update stock count and sales for the product
                product.stock_count += order_item.qty  # Return the quantity to stock
                product.sold_item -= order_item.qty  # Reduce sold items count
                product.total_product_sale -= order_item.total  # Deduct sales amount
                product.save()

                # Update sales for the vendor
                vendor = product.vendor
                vendor.sales -= order_item.total
                vendor.save()

                return JsonResponse({'message': 'Order canceled successfully'})
            except Product.DoesNotExist:
                return JsonResponse({'message': 'Product not found'})
        else:
            return JsonResponse({'message': 'Order is already canceled'})
    return JsonResponse({'message': 'Invalid request'}, status=400)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = wishlist_model.objects.filter(user=request.user)
    wishlist_d = wishlist_model.objects.get(id=pid)
    delete_product = wishlist_d.delete()

    context = {
        "bool": True,
        "w": wishlist
    }
    wishlist_json = serializers.serialize('json', wishlist)
    t = render_to_string("core/async/wishlist-list.html", context)
    return JsonResponse({'data': t, 'w': wishlist_json})


def about_us(request):
    return render(request, 'core/about-us.html')

def terms_condition(request):
    return render(request, 'core/terms.html')
