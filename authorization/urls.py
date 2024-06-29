from django.urls import path
from .views import CustomerLoginView, home, register, logout_view


urlpatterns = [
    path("", home, name="home"),
    path('register', register, name='register'),
    path('login/', CustomerLoginView.as_view(), name='login'),  # Проверьте, что путь правильный
    path('logout/', logout_view, name='logout'),
]