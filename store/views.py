from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem

def store_view(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        order_item.quantity += quantity
        order_item.save()
    return redirect('cart')

@login_required
def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    items = order.orderitem_set.all()
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

@login_required
def checkout(request):
    order = get_object_or_404(Order, user=request.user, complete=False)
    if request.method == 'POST':
        # Simulate payment processing
        order.complete = True
        order.save()
        return redirect('order_confirmation')
    context = {'order': order}
    return render(request, 'store/checkout.html', context)

@login_required
def order_confirmation(request):
    return render(request, 'store/order_confirmation.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user, complete=True)
    context = {'orders': orders}
    return render(request, 'store/order_history.html', context)
