import json
from django.http import HttpResponse
from .models import ThemeConfig


def theme_css(request):
    config = ThemeConfig.objects.first()

    if config:
        try:
            variables = json.loads(config.css_variables)
            css_variables = "\n".join([f"--{key}: {value};" for key, value in variables.items()])
            css_content = f"""
            /* Theme configuration */
            :root {{
              /* Color & Design Token Configuration */
                {css_variables}
              /* Additional Variables */
              {config.additional_variables}
            }}
            """
            
            # Global CSS
            css_content += f"""
            \n\n/* Global CSS */
            {config.global_css}
            """

            # Custom Logo
            custom_logo_url = config.logo if config.logo else ""
            if custom_logo_url:
                css_content += f"""
                \n\n/* Custom Logo */\n
                \n.logo.logo--custom {{
                  background-image: url({custom_logo_url});
                }}
                """

            # Custom Background
            custom_background_url = config.background if config.background else ""
            if custom_background_url:
                css_content += f"""
                \n\n/* Custom Background */\n
                \n.aha__page.aha__page--custom {{
                  background-image: url({custom_background_url});
                  position: relative;
                }}
                """

                # ::before should show a black to transparent gradient
                css_content += f"""
                \n\n/* Custom Background Gradient */\n
                \n.aha__page.aha__page--custom::before {{
                  content: "";
                  position: absolute;
                  top: 0;
                  right: 0;
                  bottom: 0;
                  left: 0;
                  background: linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0) 100%);
                }}
                """

        except json.JSONDecodeError:
            # Handle the case where JSON is not well-formatted
            css_content = "/* Error in CSS variables JSON format */"
    else:
        css_content = "/* No theme configuration found */"

    return HttpResponse(css_content, content_type="text/css")