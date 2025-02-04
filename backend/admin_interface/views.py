from django.http import HttpResponse
from .models import AdminInterfaceConfiguration


def get_theme_stylesheet(request):
    # Fetch the current theme settings
    config = AdminInterfaceConfiguration.objects.filter(active=True).first()

    if not config:
        # If no configuration is found, return an empty response
        return HttpResponse("", content_type="text/css")

    theme = config.theme if hasattr(config, 'theme') else None

    if not theme:
        # If no theme settings are found, return an empty response
        return HttpResponse("", content_type="text/css")

    # Create the stylesheet content
    stylesheet_content = f""":root {{
    /* Official Django colors */
    --primary: {theme.color_primary};
    --secondary: {theme.color_secondary};
    --accent: {theme.color_accent};
    --primary-fg: {theme.color_primary_fg};

    /* Body */
    --body-fg: {theme.color_body_fg};
    --body-bg: {theme.color_body_bg};
    --body-quiet-color: {theme.color_body_quiet_color};
    --body-loud-color: {theme.color_body_loud_color};

    /* Header */
    --header-color: {theme.color_header_color};

    /* Breadcrumbs */
    --breadcrumbs-fg: {theme.color_breadcrumbs_fg};

    /* Link */
    --link-fg: {theme.color_link_fg};
    --link-hover-color: {theme.color_link_hover_color};
    --link-selected-fg: {theme.color_link_selected_fg};

    /* Borders */
    --hairline-color: {theme.color_hairline_color};
    --border-color: {theme.color_border_color};

    /* Error */
    --error-fg: {theme.color_error_fg};

    /* Message */
    --message-success-bg: {theme.color_message_success_bg};
    --message-warning-bg: {theme.color_message_warning_bg};
    --message-error-bg: {theme.color_message_error_bg};

    /* Darkened */
    --darkened-bg: {theme.color_darkened_bg};

    /* Selected */
    --selected-bg: {theme.color_selected_bg};
    --selected-row: {theme.color_selected_row};

    /* Button */
    --button-fg: {theme.color_button_fg};
    --button-bg: {theme.color_button_bg};
    --button-hover-bg: {theme.color_button_hover_bg};
    --default-button-bg: {theme.color_default_button_bg};
    --default-button-hover-bg: {theme.color_default_button_hover_bg};
    --close-button-bg: {theme.color_close_button_bg};
    --close-button-hover-bg: {theme.color_close_button_hover_bg};
    --delete-button-bg: {theme.color_delete_button_bg};
    --delete-button-hover-bg: {theme.color_delete_button_hover_bg};

    /* Custom colors */
    --default-bg: {theme.color_default_bg};
    --default-fg: {theme.color_default_fg};
    --success-bg: {theme.color_success_bg};
    --success-fg: {theme.color_success_fg};
    --warning-bg: {theme.color_warning_bg};
    --warning-fg: {theme.color_warning_fg};
    --error-bg: {theme.color_error_bg};
    --error-fg: {theme.color_error_fg};
}}
"""

    # Return as CSS content
    return HttpResponse(stylesheet_content, content_type="text/css")
