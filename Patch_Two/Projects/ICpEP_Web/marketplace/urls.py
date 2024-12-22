from django.urls import path
from . import views

app_name = 'marketplace'
urlpatterns = [
    # Admin views for managing the marketplace
    path('marketplace/', views.admin_marketplace, name='admin_marketplace'),
    path('marketplace/add/', views.add_product, name='add_product'),
    path('marketplace/product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('marketplace/product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('marketplace/product/<int:product_id>/orders/', views.product_orders, name='product_orders'),
    path('marketplace/user/carts/', views.view_user_carts, name='view_user_carts'),

    # Student views for browsing products and managing cart
    path('student/marketplace/', views.student_marketplace, name='student_marketplace'),
    path('student/marketplace/<int:product_id>/order/', views.order_product, name='order_product'),
    path('student/marketplace/cart/', views.view_cart, name='view_cart'),
    path('student/marketplace/cart/<int:cart_id>/edit/', views.edit_order, name='edit_order'),
    path('student/marketplace/cart/<int:cart_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('student/marketplace/<int:product_id>/', views.student_view_product, name='student_view_product'),
    path('student/marketplace/cart/<int:cart_id>/mark_received/', views.mark_order_received, name='mark_order_received')
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
