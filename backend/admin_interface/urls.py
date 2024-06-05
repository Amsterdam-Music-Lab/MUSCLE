from django.urls import path

from .views import get_theme_stylesheet

app_name = 'admin_interface'

urlpatterns = [
    path('theme.css', get_theme_stylesheet, name='get_theme_stylesheet'),
]
