from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from .models import Recipe, Rating


class RecipeList(generic.ListView):

    model = Recipe
    queryset = Recipe.objects.all().order_by('-created_on')
    template_name = "index.html"
    paginated_by = 6
    

def full_recipe(request, slug, *args, **kwargs):
    """
    A function-based view to view the detail of a post.
    Largely the same as the class-based, but we don't have
    different methods for GET and POST. Because it's not a
    class, all of the extra "self" stuff is removed too.

    Functionally, it's the same, but it is a bit clearer
    what's going on. To differentiate between request methods,
    we use request.method == "GET" or request.method == "POST"
    """

    queryset = Recipe.objects.all()
    recipe = get_object_or_404(queryset, slug=slug)
    comments = recipe.comments.all().order_by("-created_on")
    comment_count = recipe.comments.filter(approved=True).count()
    liked = False
    #commented = False

    if recipe.likes.filter(id=request.user.id).exists():
        liked = True

    # if request.method == "POST":
    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():
    #         comment_form.instance.email = request.user.email
    #         comment_form.instance.name = request.user.username
    #         comment = comment_form.save(commit=False)
    #         comment.recipe = recipe
    #         comment.save()
    #         messages.add_message(request, messages.SUCCESS, 'Comment awaiting moderation.')
    #     else:
    #         comment_form = CommentForm()
    # else:
    #     comment_form = CommentForm()

    return render(
        request,
        "full_recipe.html",
        {
            "recipe": recipe,
            "comments": comments,
            "comment_count": comment_count,
            "liked": liked,
           # "comment_form": comment_form
        },
    )
