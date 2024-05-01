from django.contrib import admin
from django.utils.html import format_html
from .models import AdminInterfaceConfiguration, AdminInterfaceThemeConfiguration
from .forms import AdminInterfaceConfigurationForm, AdminInterfaceThemeConfigurationForm


class AdminInterfaceThemeConfigurationInline(admin.StackedInline):
    model = AdminInterfaceThemeConfiguration
    form = AdminInterfaceThemeConfigurationForm
    extra = 0
    fields = (
        # Color scheme

        ## Official Django colors

        ### Main colors
        'color_primary',
        'color_secondary',
        'color_accent',
        'color_primary_fg',

        ### Body
        'color_body_fg',
        'color_body_bg',
        'color_body_quiet_color',
        'color_body_loud_color',

        ### Header
        'color_header_color',

        ### Breadcumbs
        'color_breadcrumbs_fg',

        ### Link
        'color_link_fg',
        'color_link_hover_color',
        'color_link_selected_fg',

        ### Borders
        'color_hairline_color',
        'color_border_color',

        ### Error
        'color_error_fg',

        ### Message
        'color_message_success_bg',
        'color_message_warning_bg',
        'color_message_error_bg',

        ### Darkened
        'color_darkened_bg',

        ### Selected
        'color_selected_bg',
        'color_selected_row',

        ### Button
        'color_button_fg',
        'color_button_bg',
        'color_button_hover_bg',
        'color_default_button_bg',
        'color_default_button_hover_bg',
        'color_close_button_bg',
        'color_close_button_hover_bg',
        'color_delete_button_bg',
        'color_delete_button_hover_bg',

        # Custom colors
        'color_default_bg',
        'color_default_fg',
        'color_success_bg',
        'color_success_fg',
        'color_warning_bg',
        'color_warning_fg',
        'color_error_bg',
    )


class AdminInterfaceConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'theme_overview', 'active',)

    form = AdminInterfaceConfigurationForm
    inlines = [AdminInterfaceThemeConfigurationInline]

    def theme_overview(self, obj):
        theme = obj.theme if hasattr(obj, 'theme') else None

        if not theme:
            return "No theme assigned"
        
        fields = AdminInterfaceThemeConfigurationInline.fields
        color_fields = [f for f in fields if f.startswith('color_')]
        color_overview = ''.join(
            f'<span style="display: inline-block; width: 20px; height: 20px; background-color: {getattr(theme, f)}; margin-right: 5px;"></span>'
            for f in color_fields
        )

        return format_html(f'<div>{color_overview}</div>')


admin.site.register(
    AdminInterfaceConfiguration,
    AdminInterfaceConfigurationAdmin,
)
