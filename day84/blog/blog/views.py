from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, Category

def post_list(request):
    q = request.GET.get("q", "")
    category = request.GET.get("category", "")

    queryset = Post.objects.select_related("category")

    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(content__icontains=q))

    if category:
        queryset = queryset.filter(category__name__iexact=category)

    paginator = Paginator(queryset, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/post_list.html", {
        "posts": page_obj.object_list,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "q": q,
        "selected_category": category,
    })
