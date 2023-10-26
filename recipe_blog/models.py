from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db.models import Avg


class RecipeMethod(models.Model):
    """
    Model representing Method of Recipe (Method type: Steam, Stir Fry etc)
    """
    recipe_method = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name = "Method"

    def __str__(self):
        return self.recipe_method


class RecipeCategory(models.Model):
    """
    Model representing category of Recipe (Food type: Rice, Curry etc)
    """
    food_type = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name = "Category"

    def __str__(self):
        return self.food_type


def field_validation(value):
    """
    Function to validate servings,estimated_time and calorie_count field values
    """
    if value == 0:
        raise ValidationError(
            ('The value should be greater than zero'),
            params={'value': value},
        )


class Recipe(models.Model):
    """
    A recipe model to publish new recipes
    """
    title = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(
        RecipeCategory, on_delete=models.PROTECT, related_name='category')
    method = models.ForeignKey(
        RecipeMethod, on_delete=models.PROTECT, related_name='method')
    slug = models.SlugField(max_length=100, unique=True)
    author_name = models.CharField(max_length=150, unique=True, default="Enter your name")
    author_email = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name='published_recipes')
    featured_image = CloudinaryField('image', default='placeholder')
    ingredients = models.TextField(blank=False)
    instructions = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    prep_time = models.PositiveIntegerField(
        'prep_time', validators=[
            field_validation, MaxValueValidator(500)])
    cooking_time = models.PositiveIntegerField(
        'cooking_time', validators=[
            field_validation, MaxValueValidator(500)])
    servings = models.PositiveIntegerField(
        'servings', validators=[field_validation, MaxValueValidator(50)])
    calories = models.PositiveIntegerField(
        'calories', validators=[field_validation, MaxValueValidator(5000)])
    likes = models.ManyToManyField(
         settings.AUTH_USER_MODEL, related_name='recipe_likes', blank=True)

    class Meta:
        ordering = ['-created_on']

    def number_of_likes(self):
        return self.likes.count()

    def average_rating(self) -> float:
        return Rating.objects.filter(recipe_id=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.author_name} | {self.title}: {self.average_rating()}"

    def save(self, *args, **kwargs):
        """
        Method to generate slug for site form
        """
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(blank=False, default=0)

    def __str__(self):
        return f"{self.recipe.title}: {self.rating}"


class Comment(models.Model):
    """
    Comment model to approved by the admin before it is published
    """
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.name} on {self.created_on}'