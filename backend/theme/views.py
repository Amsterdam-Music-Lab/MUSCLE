from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from theme.models import ThemeConfig
from theme.serializers import serialize_theme


def get_theme(request, theme_id):
    theme = get_object_or_404(ThemeConfig, pk=theme_id)
    return JsonResponse(serialize_theme(theme))
