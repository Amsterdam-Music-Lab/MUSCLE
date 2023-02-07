from django.urls import path

from result.views import current_profile, consent, get_result, score

app_name = 'result'

urlpatterns = [
     path('current_profile/', current_profile,
         name='current_profile'),
     path('score/', score,
         name='result_score'),
     path('consent/', consent,
          name='register_consent'),
     path('<slug:question>/', get_result,
         name='result_get'),
]