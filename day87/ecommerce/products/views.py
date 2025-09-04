from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, CustomerQueryForm
from .models import Order

# -------------------------------
# HOME
# -------------------------------
def home(request):
    return render(request, 'products/home.html')


# -------------------------------
# USER REGISTRATION
# -------------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect('place_order')
    else:
        form = UserRegisterForm()
    return render(request, 'products/register.html', {'form': form})


# -------------------------------
# LOGIN
# -------------------------------
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'products/login.html', {'form': form})


# -------------------------------
# LOGOUT (POST for safety)
# -------------------------------
from django.views.decorators.http import require_POST

@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


# -------------------------------
# PLACE ORDER
# -------------------------------
@login_required
def place_order(request):
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            order_id=f"ORD{Order.objects.count() + 1:05d}",
            total_amount=request.POST.get('total_amount', 0)
        )

        # Send confirmation email to user
        send_mail(
            subject=f"Order Confirmation #{order.order_id}",
            message=(
                f"Hello {request.user.username},\n\n"
                f"Your order #{order.order_id} has been placed successfully.\n"
                f"Total Amount: ${order.total_amount}\n\n"
                f"Thank you for shopping with us!"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=False,
        )
        return redirect('order_success', order_id=order.id)

    return render(request, 'products/place_order.html')


# -------------------------------
# ORDER SUCCESS PAGE
# -------------------------------
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'products/order_success.html', {'order': order})


# -------------------------------
# CUSTOMER QUERY
# -------------------------------
@login_required
def customer_query(request):
    if request.method == 'POST':
        form = CustomerQueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.user = request.user
            query.save()

            # Email admin about query
            send_mail(
                subject=f"New Customer Query from {query.name}",
                message=f"Name: {query.name}\nEmail: {query.email}\nMessage: {query.message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return redirect('query_success')
    else:
        form = CustomerQueryForm()
    return render(request, 'products/customer_query.html', {'form': form})


@login_required
def query_success(request):
    return render(request, 'products/query_success.html')
