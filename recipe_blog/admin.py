from django.contrib import admin
from .models import Recipe, Comment, RecipeMethod, RecipeCategory, Rating
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'category', 'method', 'created_on')
    search_fields = ['title', 'category', 'method']
    list_filter = ('created_on', 'category', 'method')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('ingredients', 'instructions',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'recipe', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


admin.site.register(RecipeMethod)
admin.site.register(RecipeCategory)
admin.site.register(Rating)