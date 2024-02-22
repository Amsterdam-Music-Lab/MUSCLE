import json
import re
from django.http import HttpResponse
from .models import ThemeConfig


def theme_css(request):
    config = ThemeConfig.objects.filter(active=True).first()

    if config:
        try:
            variables = json.loads(config.css_variables)
            css_variables = "\n\t".join([f"--{key}: {value};" for key, value in variables.items() if value and value.strip() != ""])

            css_content = "/* Theme configuration */\n"

            # Custom Fonts
            custom_font = config.font if config.font else ""
            if custom_font:
                # Check if the font field contains a URL
                if custom_font.startswith('http://') or custom_font.startswith('https://'):
                    # Extract font-family name from URL
                    font_family_match = re.search(r'family=([^&:]+)', custom_font)
                    font_family = font_family_match.group(1).replace("+", " ") if font_family_match else "sans-serif"

                    css_content += f"""
                    /* Custom Font */
                    @import url('{custom_font}');
                    body.root {{
                      font-family: '{font_family}';
                    }}
                    """
                else:
                    # Font is specified as a Google Font name
                    css_content += f"""
                    /* Custom Font */
                    @import url('https://fonts.googleapis.com/css2?family={custom_font}&display=swap');
                    body.root {{
                      font-family: '{custom_font}';
                    }}
                    """

            # CSS Variables
            css_content += f"""
            /* CSS Variables */
            :root {{
              /* Color & Design Token Configuration */
                {css_variables}

              /* Additional Variables */
                {config.additional_variables}
            }}
            """
            
            # Global CSS
            if config.global_css:
                css_content += f"""
                /* Global CSS */
                {config.global_css}
                """

            # Custom Logo
            custom_logo_url = config.logo if config.logo else ""
            if custom_logo_url:
                css_content += f"""
                /* Custom Logo */
                .logo.logo--custom {{
                  background-image: url({custom_logo_url}) !important;
                }}
                """

            # Custom Background
            custom_background_url = config.background if config.background else ""
            if custom_background_url:
                css_content += f"""
                /* Custom Background */\n
                .aha__page.aha__page--custom {{
                  background-image: url({custom_background_url});
                  position: relative;
                }}
                """

                # ::before should show a black to transparent gradient
                css_content += """
                /* Custom Background Gradient */
                .aha__page.aha__page--custom::before {
                  content: "";
                  position: absolute;
                  top: 0;
                  right: 0;
                  bottom: 0;
                  left: 0;
                  background: linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0) 100%);
                }
                """

        except json.JSONDecodeError:
            # Handle the case where JSON is not well-formatted
            css_content = "/* Error in CSS variables JSON format */"
    else:
        css_content = "/* No theme configuration found */"

    return HttpResponse(css_content, content_type="text/css")