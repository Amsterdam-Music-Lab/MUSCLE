import json
from django.http import HttpResponse
from .models import ThemeConfig

def theme_css(request):
    config = ThemeConfig.objects.first()

    if config:
        try:
            variables = json.loads(config.css_variables)
            css_content = "\n".join([f"--{key}: {value};" for key, value in variables.items()])
            css_content += "\n" + config.additional_variables
            css_content += "\n" + config.global_css
        except json.JSONDecodeError:
            # Handle the case where JSON is not well-formatted
            css_content = "/* Error in CSS variables JSON format */"
    else:
        css_content = "/* No theme configuration found */"

    return HttpResponse(css_content, content_type="text/css")
