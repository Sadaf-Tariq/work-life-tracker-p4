from django.shortcuts import render
from django.views import generic
from .models import Recipe, Rating

class RecipeList(generic.ListView):

    model = Recipe
    queryset = Recipe.objects.all().order_by('-created_on')
    template_name = "index.html"
    paginated_by = 6
