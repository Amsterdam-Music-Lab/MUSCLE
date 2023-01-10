from django.urls import path

from result.views import current_profile, create, get_result

app_name = 'result'

urlpatterns = [
    path('current_profile/', current_profile,
         name='current_profile'),
    path('create/', create,
         name='result_create'),
    path('<slug:question>/', get_result,
         name='result_get'),
]