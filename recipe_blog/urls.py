from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('rate/<int:recipe_id>/<int:rating>/', views.rate),
]