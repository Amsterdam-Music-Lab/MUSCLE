from django.http import JsonResponse
from question.models import QuestionGroup


def question_groups(request):
    question_groups = {}
    for question_group in QuestionGroup.objects.all():
        question_groups[question_group.key] = [q.key for q in QuestionGroup.objects.get(pk=question_group.key).questions.all()]
    return JsonResponse(question_groups)
