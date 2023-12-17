from django.urls import path
from .views import theme_css

app_name='theme'

urlpatterns = [
    path('theme.css', theme_css, name='theme-css')
]
