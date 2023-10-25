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
    Method = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name = ""

    def __str__(self):
        return self.Method


class RecipeCategory(models.Model):
    """
    Model representing category of Recipe (Food type: Rice, Curry etc)
    """
    food_type = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name = ""

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
        RecipeCategory, on_delete=models.CASCADE, related_name='category')
    method = models.ForeignKey(
        RecipeMethod, on_delete=models.CASCADE, related_name='method')
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='published_recipes')
    featured_image = CloudinaryField('image', default='placeholder')
    ingredients = models.TextField(blank=False)
    instructions = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    estimated_time = models.PositiveIntegerField(
        'estimated_time', validators=[
            validate_nonzero, MaxValueValidator(600)])
    servings = models.PositiveIntegerField(
        'servings', validators=[validate_nonzero, MaxValueValidator(50)])
    calories = models.PositiveIntegerField(
        'servings', validators=[validate_nonzero, MaxValueValidator(50)])
    likes = models.ManyToManyField(
        User, related_name='recipe_likes', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.title} | {self.author}'

    def number_of_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        """
        A method to generate slug for recipes
        submitted through the site form
        """
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)



class Comment(models.Model):
    """
    A comment model
    Before the comment is published, it needs to be approved by the admin
    """
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.name}'