from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Recipe
from .forms import RecipeForm, RecipeSearchForm

# ---------------- Home / ListView ----------------
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Recipe.objects.filter(title__icontains=query)
        return Recipe.objects.all().order_by('-created_at')

# ---------------- DetailView ----------------
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

# ---------------- Submit Recipe ----------------
@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, "Recipe submitted successfully!")
            return redirect('recipes:recipe_list')
        else:
            messages.error(request, "Error submitting recipe. Check the form.")
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})

# ---------------- Edit Recipe ----------------
@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe updated successfully!")
            return redirect('recipes:recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form})

# ---------------- Delete Recipe ----------------
@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    recipe.delete()
    messages.success(request, "Recipe deleted successfully!")
    return redirect('recipes:recipe_list')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)  # log in the user immediately after registration
            messages.success(request, "Registration successful!")
            return redirect('recipes:recipe_list')

    return render(request, "register.html")
