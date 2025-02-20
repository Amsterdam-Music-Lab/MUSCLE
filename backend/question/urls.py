from django.urls import path, include
from rest_framework import routers
from .views import question_groups, QuestionViewSet

app_name = "question"

router = routers.DefaultRouter()
router.register(r"question_groups", viewset=question_groups, basename="question_groups")

api_router = routers.DefaultRouter()
api_router.register(r"questions", QuestionViewSet, basename="question")

urlpatterns = [
    path("question_groups/", question_groups, name="question_groups"),
    path("api/", include(api_router.urls)),
]
