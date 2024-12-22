from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Cart
from .forms import OrderForm, ProductForm, SearchCartForm, ProductImage
from accounts.decorators import role_required


@login_required
@role_required('student')
def student_marketplace(request):
    """
    Lists all products and their stock availability with a representative photo.
    """
    products = Product.objects.prefetch_related('images').all()
    return render(request, 'marketplace/student/student_marketplace.html', {'products': products})


@login_required
@role_required('student')
def order_product(request, product_id):
    """
    Responsible for ordering or pre-ordering products and reducing stock if applicable.
    """
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product

            if product.tag == 'Pre-orderable' or product.is_stock_available(order.quantity):
                if product.tag != 'Pre-orderable':
                    product.quantity -= order.quantity  # Deduct stock for non-pre-orderable items
                    product.save()
                order.save()
                return redirect('view_cart')
            else:
                form.add_error(None, "Insufficient stock available.")
    else:
        form = OrderForm()
    return render(request, 'marketplace/student/order_product.html', {
        'form': form,
        'product': product,
        'is_preorder': product.tag == 'Pre-orderable'
    })

@login_required
@role_required('student')
def view_cart(request):
    """
    Responsible for viewing the cart and order statuses.
    Excludes orders marked as 'Received' for students.
    """
    cart_items = Cart.objects.filter(user=request.user).exclude(order_status='Received').order_by('-order_date')
    return render(request, 'marketplace/student/view_cart.html', {'cart_items': cart_items})

@login_required
@role_required('student')
def edit_order(request, cart_id):
    cart_item = get_object_or_404(Cart, cart_id=cart_id)
    old_quantity = cart_item.quantity  # Save the original quantity before editing
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=cart_item)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            product = cart_item.product

            # Calculate the stock adjustment
            quantity_difference = new_quantity - old_quantity
            
            # Check if the product stock is sufficient for the update
            if quantity_difference > 0 and not product.is_stock_available(quantity_difference):
                form.add_error('quantity', 'Not enough stock available for the updated quantity.')
            else:
                # Update product stock
                product.quantity -= quantity_difference
                product.save()

                # Save the updated cart item
                form.save()
                return redirect('view_cart')
    else:
        form = OrderForm(instance=cart_item)
    
    return render(request, 'marketplace/student/edit_order.html', {'form': form, 'cart_item': cart_item})

@login_required
@role_required('student')
def cancel_order(request, cart_id):
    """
    Allows students to cancel an order from their cart.
    """
    cart_item = get_object_or_404(Cart, cart_id=cart_id)

    # Restore stock for the cancelled order
    product = cart_item.product
    product.quantity += cart_item.quantity
    product.save()

    # Cancel the cart item
    cart_item.delete()
    return redirect('view_cart')

@login_required
@role_required('student')
def mark_order_received(request, cart_id):
    """
    Marks an order as received and removes it from the student's cart view,
    while keeping it visible in the admin's view.
    """
    cart_item = get_object_or_404(Cart, cart_id=cart_id)

    if cart_item.user == request.user:
        # Update the order status to 'Received'
        cart_item.order_status = 'Received'
        cart_item.save()

        # Remove the order from the student's cart by filtering in the view
        return redirect('view_cart')
    else:
        return redirect('view_cart')  # Optional: Add error handling here.

@login_required
@role_required('student')
def student_view_product(request, product_id):
    """
    Displays detailed information about a selected product, including all its photos.
    """
    product = get_object_or_404(Product.objects.prefetch_related('images'), product_id=product_id)
    images = product.images.all()  # Get all related images
    return render(request, 'marketplace/student/student_view_product.html', {
        'product': product,
        'images': images,
    })



from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required
@role_required('admin')
def admin_marketplace(request):
    products = Product.objects.all()


    # Standard rendering for non-AJAX requests
    return render(request, 'marketplace/admin/admin_marketplace.html', {'products': products})

@login_required
@role_required('admin')
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        images = request.FILES.getlist('images')  # Get all uploaded images

        if product_form.is_valid():
            product = product_form.save()  # Save the product

            # Create a ProductImage for each uploaded image
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            return JsonResponse({'success': True})  # Redirect to the product list after creation
        

    else:
        product_form = ProductForm()

    return render(request, 'marketplace/admin/add_product.html', {'product_form': product_form})

@login_required
@role_required('admin')
def edit_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        # Bind the form with the posted data and files
        product_form = ProductForm(request.POST, request.FILES, instance=product)

        if product_form.is_valid():
            product_form.save()  # Save product changes

            # Handle new images if any are uploaded
            images = request.FILES.getlist('images')  # Fetch uploaded images
            for image in images:
                ProductImage.objects.create(product=product, image=image)  # Create image entries
            
            # Optionally, add logic to delete selected images if needed

            return redirect('admin_marketplace')
    else:
        product_form = ProductForm(instance=product)

    # Fetch existing images related to the product
    existing_images = product.images.all()

    return render(request, 'marketplace/admin/edit_product.html', {
        'form': product_form,
        'product': product,
        'existing_images': existing_images,
    })



@login_required
@role_required('admin')
def delete_product(request, product_id):
    """
    Allows admin to delete a product.
    """
    product = get_object_or_404(Product, product_id=product_id)
    product.delete()
    return redirect('admin_marketplace')


@login_required
@role_required('admin')
def product_orders(request, product_id):
    """
    Displays all orders for a specific product with optional year and block filtering.
    """
    product = get_object_or_404(Product, product_id=product_id)
    
    # Debug: Check if product is correctly retrieved and has an id
    print("Product ID:", product.product_id)

    orders = Cart.objects.filter(product=product)

    # Filter by acad_year if provided
    year_filter = request.GET.get('acad_year')
    if year_filter:
        # Debug: Log the year filter
        print("Year filter received:", year_filter)
        orders = orders.filter(user__acad_year=year_filter)

    # Filter by acad_block if provided
    block_filter = request.GET.get('acad_block')
    if block_filter:
        # Debug: Log the block filter
        print("Block filter received:", block_filter)
        orders = orders.filter(user__acad_block=block_filter)

    # Debug: Log order count after applying filters
    print("Order count after filters:", orders.count())

    return render(request, 'marketplace/admin/product_orders.html', {'product': product, 'orders': orders})

@login_required
@role_required('admin')
def view_user_carts(request):
    """
    Displays all user carts for admin management with optional filters for name, year, and block.
    """
    form = SearchCartForm(request.GET)
    carts = Cart.objects.all().order_by('-order_date')  # Default ordering by order_date

    # Apply filters based on form data
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        acad_year = form.cleaned_data.get('acad_year')
        acad_block = form.cleaned_data.get('acad_block')

        # Filter by student name if provided
        if search_query:
            carts = carts.filter(
                Q(user__last_name__icontains=search_query) |
                Q(user__given_name__icontains=search_query)
            )

        # Filter by academic year if provided
        if acad_year:
            carts = carts.filter(user__acad_year=acad_year)

        # Filter by academic block if provided
        if acad_block:
            carts = carts.filter(user__acad_block=acad_block)

    empty_message = 'Student not found.'
    return render(request, 'marketplace/admin/user_carts.html', {'carts': carts, 'form': form, 'empty_message': empty_message})