from django.urls import path

from result.views import current_profile, create, get_result

app_name = 'result'

urlpatterns = [
    # Profile
    path('result/current_profile', current_profile,
         name='current_profile'),
    path('result/create/', create,
         name='result_create'),
    path('result/<slug:question>/', get_result,
         name='result_get'),
]