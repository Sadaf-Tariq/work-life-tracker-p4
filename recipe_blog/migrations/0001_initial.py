# Generated by Django 3.2.22 on 2023-10-26 10:01

import cloudinary.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipe_blog.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_type', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '',
            },
        ),
        migrations.CreateModel(
            name='RecipeMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Method', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('featured_image', cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image')),
                ('ingredients', models.TextField()),
                ('instructions', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('prep_time', models.PositiveIntegerField(validators=[recipe_blog.models.field_validation, django.core.validators.MaxValueValidator(500)], verbose_name='prep_time')),
                ('cooking_time', models.PositiveIntegerField(validators=[recipe_blog.models.field_validation, django.core.validators.MaxValueValidator(500)], verbose_name='cooking_time')),
                ('servings', models.PositiveIntegerField(validators=[recipe_blog.models.field_validation, django.core.validators.MaxValueValidator(50)], verbose_name='servings')),
                ('calories', models.PositiveIntegerField(validators=[recipe_blog.models.field_validation, django.core.validators.MaxValueValidator(50)], verbose_name='calories')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='published_recipes', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='category', to='recipe_blog.recipecategory')),
                ('likes', models.ManyToManyField(blank=True, related_name='recipe_likes', to=settings.AUTH_USER_MODEL)),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='method', to='recipe_blog.recipemethod')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(default=0)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_blog.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='recipe_blog.recipe')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
