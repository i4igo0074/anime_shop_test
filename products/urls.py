
from django.urls import path
from . import views
from .views import toggle_favorite



urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('toggle_favorite/<int:product_id>/', toggle_favorite, name='toggle_favorite'),
    path('favorites', views.favorites, name='favorites'),
    path('collection/', views.collection, name='collection'),
    path('collection/<int:collection_id>/', views.collection_detail, name='collection_detail'),  # Пример URL-шаблона для collection_detail
]
