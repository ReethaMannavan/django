from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'steps', 'image', 'category']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows':4}),
            'steps': forms.Textarea(attrs={'rows':6}),
        }

class RecipeSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search Recipes')
