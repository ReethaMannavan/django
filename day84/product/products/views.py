from django.shortcuts import render

# Create your views here.
# products/views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product

def product_list(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    availability = request.GET.get('availability')

    products = Product.objects.all()

    # Search
    if query:
        products = products.filter(Q(name__icontains=query) | Q(brand__icontains=query))

    # Filter by price
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Filter by availability
    if availability == 'available':
        products = products.filter(is_available=True)
    elif availability == 'unavailable':
        products = products.filter(is_available=False)

    # Pagination
    paginator = Paginator(products, 10)  # 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_results = products.count()

    context = {
        'page_obj': page_obj,
        'total_results': total_results,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'availability': availability,
    }
    return render(request, 'products/product_list.html', context)
