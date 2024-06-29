# mainapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-company/', views.about_company, name='about-company'),
]
