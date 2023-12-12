from django.urls import path, include
from core.views import index, order_detail, index2, render_order_notification ,cancel_order, remove_wishlist ,redirect_to_multiple_urls, add_to_wishlist ,wishlist_view,  make_address_default , customer_dashboard, category_list_view, product_list_view, category_product_list__view, vendor_list_view, vendor_detail_view, product_detail_view, ajax_add_review, search_view, filter_product, add_to_cart, cart_view, checkout_view, payment_completed_view, payment_failed_view, delete_item_from_cart, update_cart, about_us, terms_condition  # Assuming your view is defined in core.views
from django.contrib.auth import views as auth_views
app_name = "core"

urlpatterns = [
    path('admin-dashboard/', index2, name='admin-dashboard'),
    path('admin/', include('admin_soft.urls')),
    #homepage
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),

    #categories
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list__view, name="category-product-list"),

    #vendors
    path("vendors/", vendor_list_view, name="vendor-list" ),
    path("vendor/<vid>/", vendor_detail_view, name="vendor-detail" ),

    #reviews
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax_add_review"),

    path("search/", search_view, name="search" ),

    path("filter-products/", filter_product, name="filter-product"),

    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    path("cart/", cart_view, name="cart"),

    path('redirect_to_multiple_urls/', redirect_to_multiple_urls, name='redirect_to_multiple_urls'),

    path("checkout/", checkout_view, name="checkout"),

    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),

    path("update-cart/", update_cart, name="update-cart"),

    path("payment-failed/", payment_failed_view, name="payment-failed"),

    path("payment-completed/", payment_completed_view, name="payment-completed"),

    path("payment-failed/", payment_failed_view, name="payment-failed"),

    path("dashboard/", customer_dashboard, name="dashboard"),

    path("dashboard/order/", order_detail, name="order-detail"),

    path("make-default-address/", make_address_default, name="make-default-address"),

    path("wishlist/", wishlist_view, name="wishlist"),

    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),

    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),

    path("about-us/", about_us, name="about-us" ),

    path("terms-&-conditions/", terms_condition, name="terms" ),

    path('cancel_order/<int:order_item_id>/', cancel_order, name='cancel_order'),

    path('email-templates/order-notification/', render_order_notification, name='order_notification'),

    # path("", include('django.contrib.auth.urls')),
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # Updated name
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    ]
