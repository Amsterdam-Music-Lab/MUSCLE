from django.urls import path

from .views import get

urlpatterns = [
# Section
    path('section/<int:section_id>/<int:code>/',
        get, name='section'),
]