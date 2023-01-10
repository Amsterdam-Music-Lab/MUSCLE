from django.urls import path

from .views import get_section

urlpatterns = [
# Section
    path('section/<int:section_id>/<int:code>/',
        get_section, name='section'),
]