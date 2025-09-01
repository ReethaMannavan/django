from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, CartItem
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

# --- Product List ---
class ProductListView(ListView):
    model = Product
    template_name = "shop_app/product_list.html"
    context_object_name = "products"

# --- Product Detail ---
class ProductDetailView(DetailView):
    model = Product
    template_name = "shop_app/product_detail.html"
    context_object_name = "product"

# --- Register ---
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("shop_app:product_list")
    else:
        form = UserCreationForm()
    return render(request, "shop_app/register.html", {"form": form})

# --- Cart ---
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect("shop_app:product_list")

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, "shop_app/cart.html", {"cart_items": cart_items})

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("shop_app:cart")
